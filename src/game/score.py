# src/game/score.py

LINE_POINTS = 10
BINGO_POINTS = 50

class ScoreTracker:
    def __init__(self):
        self.score = 0
        self.lines_done = 0
        self.has_bingo = False

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

    def get_score(self):
        return self.score
