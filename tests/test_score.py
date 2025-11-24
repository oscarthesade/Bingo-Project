"""
Comprehensive tests for ScoreTracker class.
Tests use mocking to avoid requiring actual Redis connection.
"""
import pytest
import os
from unittest.mock import Mock, MagicMock, patch, call
from src.game.score import ScoreTracker, LINE_POINTS, BINGO_POINTS


class TestScoreTrackerInitialization:
    """Test ScoreTracker initialization."""
    
    @patch('src.game.score.redis.Redis')
    def test_init_with_redis_connection(self, mock_redis_class, mock_redis_client):
        """Test initialization when Redis is available."""
        mock_redis_class.return_value = mock_redis_client
        mock_redis_client.ping.return_value = True
        
        tracker = ScoreTracker()
        assert tracker.score == 0
        assert tracker.lines_done == 0
        assert tracker.has_bingo is False
        assert tracker.redis_client is not None
        mock_redis_client.ping.assert_called_once()
    
    @patch('src.game.score.redis.Redis')
    def test_init_without_redis_connection(self, mock_redis_class):
        """Test initialization when Redis is unavailable."""
        mock_redis_class.side_effect = Exception("Connection failed")
        
        tracker = ScoreTracker()
        assert tracker.score == 0
        assert tracker.lines_done == 0
        assert tracker.has_bingo is False
        assert tracker.redis_client is None
    
    @patch('src.game.score.redis.Redis')
    @patch.dict(os.environ, {'REDIS_HOST': 'custom-host', 'REDIS_PORT': '6380'})
    def test_init_with_custom_redis_config(self, mock_redis_class, mock_redis_client):
        """Test initialization with custom Redis host/port from environment."""
        mock_redis_class.return_value = mock_redis_client
        mock_redis_client.ping.return_value = True
        
        tracker = ScoreTracker()
        mock_redis_class.assert_called_once_with(
            host='custom-host',
            port=6380,
            decode_responses=True,
            socket_connect_timeout=5
        )


class TestUpdateScore:
    """Test score update logic."""
    
    @patch('src.game.score.redis.Redis')
    def test_update_score_no_lines(self, mock_redis_class, mock_redis_client, empty_marked_card):
        """Test score update with no complete lines."""
        mock_redis_class.return_value = mock_redis_client
        mock_redis_client.ping.return_value = True
        
        tracker = ScoreTracker()
        tracker.update_score(empty_marked_card)
        assert tracker.score == 0
        assert tracker.lines_done == 0
    
    @patch('src.game.score.redis.Redis')
    def test_update_score_one_line(self, mock_redis_class, mock_redis_client, one_line_marked):
        """Test score update with one complete line."""
        mock_redis_class.return_value = mock_redis_client
        mock_redis_client.ping.return_value = True
        
        tracker = ScoreTracker()
        tracker.update_score(one_line_marked)
        assert tracker.score == LINE_POINTS  # 10 points
        assert tracker.lines_done == 1
    
    @patch('src.game.score.redis.Redis')
    def test_update_score_two_lines(self, mock_redis_class, mock_redis_client):
        """Test score update with two complete lines."""
        mock_redis_class.return_value = mock_redis_client
        mock_redis_client.ping.return_value = True
        
        marked = [[True] * 5, [True] * 5, [False] * 5]
        tracker = ScoreTracker()
        tracker.update_score(marked)
        assert tracker.score == LINE_POINTS * 2  # 20 points
        assert tracker.lines_done == 2
    
    @patch('src.game.score.redis.Redis')
    def test_update_score_incremental(self, mock_redis_class, mock_redis_client):
        """Test that score increments correctly with multiple updates."""
        mock_redis_class.return_value = mock_redis_client
        mock_redis_client.ping.return_value = True
        
        tracker = ScoreTracker()
        # First update: one line
        marked_one = [[True] * 5, [False] * 5, [False] * 5]
        tracker.update_score(marked_one)
        assert tracker.score == LINE_POINTS
        
        # Second update: two lines (one new)
        marked_two = [[True] * 5, [True] * 5, [False] * 5]
        tracker.update_score(marked_two)
        assert tracker.score == LINE_POINTS * 2
    
    @patch('src.game.score.redis.Redis')
    def test_update_score_bingo(self, mock_redis_class, mock_redis_client, all_lines_marked):
        """Test score update when bingo is achieved."""
        mock_redis_class.return_value = mock_redis_client
        mock_redis_client.ping.return_value = True
        mock_redis_client.get.return_value = None
        
        tracker = ScoreTracker()
        tracker.update_score(all_lines_marked)
        # Should have: 3 lines * 10 points + 50 bingo bonus = 80 points
        assert tracker.score == (LINE_POINTS * 3) + BINGO_POINTS
        assert tracker.has_bingo is True
        assert tracker.lines_done == 3
    
    @patch('src.game.score.redis.Redis')
    def test_update_score_bingo_saves_to_redis(self, mock_redis_class, mock_redis_client, all_lines_marked):
        """Test that bingo triggers save to Redis."""
        mock_redis_class.return_value = mock_redis_client
        mock_redis_client.ping.return_value = True
        mock_redis_client.get.return_value = None
        
        tracker = ScoreTracker()
        tracker.update_score(all_lines_marked)
        
        # Should have called lpush for game history
        assert mock_redis_client.lpush.called
        # Should have called set for high score
        assert mock_redis_client.set.called
    
    @patch('src.game.score.redis.Redis')
    def test_update_score_bingo_only_once(self, mock_redis_class, mock_redis_client, all_lines_marked):
        """Test that bingo bonus is only added once."""
        mock_redis_class.return_value = mock_redis_client
        mock_redis_client.ping.return_value = True
        mock_redis_client.get.return_value = None
        
        tracker = ScoreTracker()
        # First update: bingo
        tracker.update_score(all_lines_marked)
        initial_score = tracker.score
        
        # Second update: still bingo, but no additional bonus
        tracker.update_score(all_lines_marked)
        assert tracker.score == initial_score  # No change


class TestGetScore:
    """Test get_score method."""
    
    @patch('src.game.score.redis.Redis')
    def test_get_score_initial(self, mock_redis_class, mock_redis_client):
        """Test getting initial score."""
        mock_redis_class.return_value = mock_redis_client
        mock_redis_client.ping.return_value = True
        
        tracker = ScoreTracker()
        assert tracker.get_score() == 0
    
    @patch('src.game.score.redis.Redis')
    def test_get_score_after_updates(self, mock_redis_class, mock_redis_client, one_line_marked):
        """Test getting score after updates."""
        mock_redis_class.return_value = mock_redis_client
        mock_redis_client.ping.return_value = True
        
        tracker = ScoreTracker()
        tracker.update_score(one_line_marked)
        assert tracker.get_score() == LINE_POINTS


class TestGetHighScore:
    """Test get_high_score method."""
    
    @patch('src.game.score.redis.Redis')
    def test_get_high_score_no_redis(self, mock_redis_class):
        """Test getting high score when Redis unavailable."""
        mock_redis_class.side_effect = Exception("Connection failed")
        
        tracker = ScoreTracker()
        assert tracker.get_high_score() == 0
    
    @patch('src.game.score.redis.Redis')
    def test_get_high_score_no_previous(self, mock_redis_class, mock_redis_client):
        """Test getting high score when none exists."""
        mock_redis_class.return_value = mock_redis_client
        mock_redis_client.ping.return_value = True
        mock_redis_client.get.return_value = None
        
        tracker = ScoreTracker()
        assert tracker.get_high_score() == 0
    
    @patch('src.game.score.redis.Redis')
    def test_get_high_score_existing(self, mock_redis_class, mock_redis_client):
        """Test getting existing high score."""
        mock_redis_class.return_value = mock_redis_client
        mock_redis_client.ping.return_value = True
        mock_redis_client.get.return_value = "100"
        
        tracker = ScoreTracker()
        assert tracker.get_high_score() == 100
    
    @patch('src.game.score.redis.Redis')
    def test_get_high_score_updates_on_bingo(self, mock_redis_class, mock_redis_client, all_lines_marked):
        """Test that high score is updated when new bingo achieved."""
        mock_redis_class.return_value = mock_redis_client
        mock_redis_client.ping.return_value = True
        mock_redis_client.get.return_value = "50"  # Lower than new score
        
        tracker = ScoreTracker()
        tracker.update_score(all_lines_marked)
        # Should have called set with new high score
        mock_redis_client.set.assert_called()
        # Get the score that was set
        set_calls = mock_redis_client.set.call_args_list
        assert any('high_score' in str(call) for call in set_calls)


class TestRedisErrorHandling:
    """Test error handling when Redis operations fail."""
    
    @patch('src.game.score.redis.Redis')
    def test_save_game_result_redis_error(self, mock_redis_class, mock_redis_client, all_lines_marked):
        """Test that game continues if Redis save fails."""
        mock_redis_class.return_value = mock_redis_client
        mock_redis_client.ping.return_value = True
        mock_redis_client.lpush.side_effect = Exception("Redis error")
        
        tracker = ScoreTracker()
        # Should not raise exception
        tracker.update_score(all_lines_marked)
        assert tracker.has_bingo is True
        assert tracker.score > 0
    
    @patch('src.game.score.redis.Redis')
    def test_get_high_score_redis_error(self, mock_redis_class, mock_redis_client):
        """Test that get_high_score handles Redis errors gracefully."""
        mock_redis_class.return_value = mock_redis_client
        mock_redis_client.ping.return_value = True
        mock_redis_client.get.side_effect = Exception("Redis error")
        
        tracker = ScoreTracker()
        # Should return 0, not raise exception
        assert tracker.get_high_score() == 0