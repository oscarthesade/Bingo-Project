"""
Comprehensive tests for BingoCard class.
"""
import pytest
from src.game.card import BingoCard


class TestBingoCardInitialization:
    """Test card initialization with different inputs."""
    
    def test_init_with_custom_numbers(self, sample_card_numbers):
        """Test card creation with custom numbers."""
        card = BingoCard(numbers=sample_card_numbers)
        assert len(card.card) == 3
        assert len(card.card[0]) == 5
        assert card.card[0][0] == 1
        assert card.card[0][4] == 5
        assert card.card[1][0] == 10
    
    def test_init_with_random_numbers(self):
        """Test card creation with random numbers."""
        card = BingoCard()
        assert len(card.card) == 3
        assert len(card.card[0]) == 5
        # Check all numbers are unique
        all_numbers = [num for row in card.card for num in row]
        assert len(all_numbers) == len(set(all_numbers))
        # Check numbers are in valid range
        assert all(1 <= num <= 75 for num in all_numbers)
    
    def test_init_creates_empty_marked(self):
        """Test that marked array is initialized as all False."""
        card = BingoCard(numbers=list(range(1, 16)))
        assert len(card.marked) == 3
        assert len(card.marked[0]) == 5
        assert all(not cell for row in card.marked for cell in row)
    
    def test_build_from_numbers_valid_input(self, sample_card_numbers):
        """Test building card from valid number list."""
        card = BingoCard(numbers=sample_card_numbers)
        assert card.card[0] == [1, 2, 3, 4, 5]
        assert card.card[1] == [10, 11, 12, 13, 14]
        assert card.card[2] == [20, 21, 22, 23, 24]
    
    def test_build_from_numbers_invalid_length(self):
        """Test that invalid number count raises ValueError."""
        with pytest.raises(ValueError, match="Expected 15 numbers"):
            BingoCard(numbers=[1, 2, 3])  # Too few numbers
    
    def test_build_from_numbers_exact_length(self):
        """Test building with exactly 15 numbers."""
        numbers = list(range(1, 16))
        card = BingoCard(numbers=numbers)
        assert len(card.card) == 3
        assert len(card.card[0]) == 5


class TestMarkNumber:
    """Test marking numbers on the card."""
    
    def test_mark_number_exists_on_card(self, sample_card_numbers):
        """Test marking a number that exists on the card."""
        card = BingoCard(numbers=sample_card_numbers)
        card.mark_number(5)
        assert card.marked[0][4] is True
        assert all(card.marked[i][j] is False 
                  for i in range(3) for j in range(5) 
                  if not (i == 0 and j == 4))
    
    def test_mark_number_not_on_card(self, sample_card_numbers):
        """Test marking a number that doesn't exist on card."""
        card = BingoCard(numbers=sample_card_numbers)
        initial_marked = [row[:] for row in card.marked]
        card.mark_number(99)  # Number not on card
        assert card.marked == initial_marked  # No changes
    
    def test_mark_multiple_numbers(self, sample_card_numbers):
        """Test marking multiple numbers."""
        card = BingoCard(numbers=sample_card_numbers)
        card.mark_number(1)
        card.mark_number(10)
        card.mark_number(20)
        assert card.marked[0][0] is True
        assert card.marked[1][0] is True
        assert card.marked[2][0] is True
    
    def test_mark_same_number_twice(self, sample_card_numbers):
        """Test marking the same number twice (should be idempotent)."""
        card = BingoCard(numbers=sample_card_numbers)
        card.mark_number(5)
        card.mark_number(5)  # Mark again
        assert card.marked[0][4] is True
        # Should still be marked, no errors


class TestHasBingo:
    """Test bingo detection logic."""
    
    def test_no_bingo_empty_card(self, sample_card_numbers):
        """Test that empty card has no bingo."""
        card = BingoCard(numbers=sample_card_numbers)
        assert card.has_bingo() is False
    
    def test_bingo_complete_row(self, sample_card_numbers):
        """Test bingo detection when a row is complete."""
        card = BingoCard(numbers=sample_card_numbers)
        # Mark first row completely
        for j in range(5):
            card.mark_number(card.card[0][j])
        assert card.has_bingo() is True
    
    def test_bingo_complete_column(self, sample_card_numbers):
        """Test bingo detection when a column is complete."""
        card = BingoCard(numbers=sample_card_numbers)
        # Mark first column completely
        for i in range(3):
            card.mark_number(card.card[i][0])
        assert card.has_bingo() is True
    
    def test_bingo_all_rows_complete(self, sample_card_numbers):
        """Test bingo when all rows are complete."""
        card = BingoCard(numbers=sample_card_numbers)
        # Mark all numbers
        for i in range(3):
            for j in range(5):
                card.mark_number(card.card[i][j])
        assert card.has_bingo() is True
    
    def test_no_bingo_partial_marking(self, sample_card_numbers):
        """Test no bingo with partial marking."""
        card = BingoCard(numbers=sample_card_numbers)
        # Mark only some numbers, not complete lines
        card.mark_number(1)
        card.mark_number(3)
        card.mark_number(10)
        assert card.has_bingo() is False


class TestCardDisplay:
    """Test card string representation."""
    
    def test_str_representation(self, sample_card_numbers):
        """Test string representation of card."""
        card = BingoCard(numbers=sample_card_numbers)
        card_str = str(card)
        assert "1" in card_str
        assert "5" in card_str
        assert "10" in card_str
        assert "24" in card_str
    
    def test_str_shows_marked_numbers(self, sample_card_numbers):
        """Test that marked numbers show checkmark."""
        card = BingoCard(numbers=sample_card_numbers)
        card.mark_number(5)
        card_str = str(card)
        # Should contain checkmark for marked number
        assert "✔" in card_str
    
    def test_str_format_consistency(self, sample_card_numbers):
        """Test that string format is consistent."""
        card = BingoCard(numbers=sample_card_numbers)
        card_str = str(card)
        lines = card_str.strip().split('\n')
        assert len(lines) == 3  # Should have 3 rows
