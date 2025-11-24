# src/game/score.py
import redis
import json
import os
from datetime import datetime

LINE_POINTS = 10
BINGO_POINTS = 50

class ScoreTracker:
    def __init__(self):
        self.score = 0
        self.lines_done = 0
        self.has_bingo = False
        
        # Get Redis configuration from environment variables
        redis_host = os.getenv('REDIS_HOST', 'redis')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        
        # Attempt to connect to Redis
        try:
            self.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                decode_responses=True,
                socket_connect_timeout=5
            )
            # Test connection
            self.redis_client.ping()
        except (redis.ConnectionError, redis.TimeoutError, Exception) as e:
            # Gracefully handle Redis unavailability
            self.redis_client = None
            if os.getenv('DEBUG', 'false').lower() == 'true':
                print(f"Redis connection failed: {e}. Running without persistence.")

    def update_score(self, marked):
        """Update the player's score based on new lines or bingo."""
        from src.game.check import count_lines, is_bingo

        current_lines = count_lines(marked)
        new_lines = current_lines - self.lines_done

        if new_lines > 0:
            self.score += new_lines * LINE_POINTS
            self.lines_done = current_lines

        if is_bingo(marked) and not self.has_bingo:
            self.score += BINGO_POINTS
            self.has_bingo = True
            self._save_game_result()

    def _save_game_result(self):
        """Save completed game to Redis."""
        if self.redis_client:
            try:
                game_data = {
                    'score': self.score,
                    'timestamp': datetime.now().isoformat(),
                    'bingo': True
                }
                self.redis_client.lpush('game_history', json.dumps(game_data))
                
                # Update high score if needed
                current_high = self.redis_client.get('high_score')
                if not current_high or int(current_high) < self.score:
                    self.redis_client.set('high_score', self.score)
            except (redis.ConnectionError, redis.TimeoutError, Exception) as e:
                # Silently fail if Redis is unavailable
                if os.getenv('DEBUG', 'false').lower() == 'true':
                    print(f"Failed to save game result: {e}")

    def get_score(self):
        return self.score

    def get_high_score(self):
        """Get high score from Redis."""
        if self.redis_client:
            try:
                high_score = self.redis_client.get('high_score')
                return int(high_score) if high_score else 0
            except (redis.ConnectionError, redis.TimeoutError, ValueError, Exception):
                return 0
        return 0
