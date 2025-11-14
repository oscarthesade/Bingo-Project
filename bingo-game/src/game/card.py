
import random

class BingoCard:
    def __init__(self, numbers=None):
        self.rows = 3
        self.cols = 5
        if numbers is None:
            self.card = self.generate_card()
        else:
            self.card = self.build_from_numbers(numbers)
        self.marked = [[False] * self.cols for _ in range(self.rows)]

    def build_from_numbers(self, numbers):
        card = []
        for i in range(self.rows):
            row = numbers[i * self.cols:(i + 1) * self.cols]
            card.append(row)
        return card

    def generate_card(self):
        # Numbers range from 1–75 (or adjust if your game rules differ)
        numbers = random.sample(range(1, 76), self.rows * self.cols)
        card = []
        for i in range(self.rows):
            row = numbers[i * self.cols:(i + 1) * self.cols]
            card.append(row)
        return card

    def mark_number(self, number):
        """Mark the number if found on the card."""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.card[i][j] == number:
                    self.marked[i][j] = True

    def has_bingo(self):
        """Check if there is a full row, column, or diagonal marked."""
        # Rows
        for row in self.marked:
            if all(row):
                return True
        # Columns
        for j in range(self.cols):
            if all(self.marked[i][j] for i in range(self.rows)):
                return True
        # Diagonals (only if square)
        if self.rows == self.cols:
            if all(self.marked[i][i] for i in range(self.rows)):
                return True
            if all(self.marked[i][self.cols - 1 - i] for i in range(self.rows)):
                return True
        return False

    def __str__(self):
        """Display the card neatly."""
        s = ""
        for i in range(self.rows):
            for j in range(self.cols):
                val = self.card[i][j]
                mark = "✔" if self.marked[i][j] else " "
                s += f"{val:>3}{mark}  "
            s += "\n"
        return s
