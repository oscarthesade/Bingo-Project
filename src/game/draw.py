import random

class NumberDrawer:
    def __init__(self, min_number=1, max_number=75):
        self.min_number = min_number
        self.max_number = max_number
        self.remaining = list(range(min_number, max_number + 1))
        random.shuffle(self.remaining)
        self.drawn_numbers = []

    def draw_number(self):
        """Draw one number randomly from remaining ones."""
        if not self.remaining:
            return None  # No numbers left
        number = self.remaining.pop()
        self.drawn_numbers.append(number)
        return number

    def get_drawn_numbers(self):
        """Return list of all drawn numbers so far."""
        return self.drawn_numbers

    def reset(self):
        """Restart the game (reshuffle)."""
        self.remaining = list(range(self.min_number, self.max_number + 1))
        random.shuffle(self.remaining)
        self.drawn_numbers = []

