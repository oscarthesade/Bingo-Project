"""
Comprehensive tests for check module functions.
"""
import pytest
from src.game.check import count_lines, is_bingo, count_diagonals


class TestCountLines:
    """Test count_lines function."""
    
    def test_count_lines_empty(self, empty_marked_card):
        """Test counting lines in empty card."""
        assert count_lines(empty_marked_card) == 0
    
    def test_count_lines_one_complete(self, one_line_marked):
        """Test counting one complete line."""
        assert count_lines(one_line_marked) == 1
    
    def test_count_lines_all_complete(self, all_lines_marked):
        """Test counting all lines complete."""
        assert count_lines(all_lines_marked) == 3
    
    def test_count_lines_partial(self, partial_marked):
        """Test counting with partial marking."""
        assert count_lines(partial_marked) == 0
    
    def test_count_lines_two_complete(self):
        """Test counting two complete lines."""
        marked = [[True] * 5, [True] * 5, [False] * 5]
        assert count_lines(marked) == 2
    
    def test_count_lines_mixed(self):
        """Test counting with mixed complete/incomplete lines."""
        marked = [
            [True] * 5,  # Complete
            [True, True, True, False, False],  # Incomplete
            [True] * 5  # Complete
        ]
        assert count_lines(marked) == 2


class TestIsBingo:
    """Test is_bingo function."""
    
    def test_is_bingo_false_empty(self, empty_marked_card):
        """Test bingo detection with empty card."""
        assert is_bingo(empty_marked_card) is False
    
    def test_is_bingo_false_one_line(self, one_line_marked):
        """Test bingo detection with one line (not bingo for 3x5)."""
        assert is_bingo(one_line_marked) is False
    
    def test_is_bingo_true_all_lines(self, all_lines_marked):
        """Test bingo detection with all lines complete."""
        assert is_bingo(all_lines_marked) is True
    
    def test_is_bingo_false_partial(self, partial_marked):
        """Test bingo detection with partial marking."""
        assert is_bingo(partial_marked) is False
    
    def test_is_bingo_two_lines_not_enough(self):
        """Test that two lines don't count as bingo."""
        marked = [[True] * 5, [True] * 5, [False] * 5]
        assert is_bingo(marked) is False
    
    def test_is_bingo_custom_size(self):
        """Test bingo with different card sizes."""
        # 2x5 card - bingo when both rows complete
        marked_2x5 = [[True] * 5, [True] * 5]
        assert is_bingo(marked_2x5) is True
        
        # 4x5 card - bingo when all 4 rows complete
        marked_4x5 = [[True] * 5 for _ in range(4)]
        assert is_bingo(marked_4x5) is True


class TestCountDiagonals:
    """Test count_diagonals function."""
    
    def test_count_diagonals_3x5_returns_zero(self, empty_marked_card):
        """Test that 3x5 cards return 0 diagonals (not square)."""
        assert count_diagonals(empty_marked_card) == 0
    
    def test_count_diagonals_square_none(self):
        """Test square card with no diagonals."""
        marked = [[False] * 3 for _ in range(3)]
        assert count_diagonals(marked) == 0
    
    def test_count_diagonals_square_main_diagonal(self):
        """Test square card with main diagonal complete."""
        marked = [[False] * 3 for _ in range(3)]
        # Mark main diagonal (top-left to bottom-right)
        for i in range(3):
            marked[i][i] = True
        assert count_diagonals(marked) == 1
    
    def test_count_diagonals_square_anti_diagonal(self):
        """Test square card with anti-diagonal complete."""
        marked = [[False] * 3 for _ in range(3)]
        # Mark anti-diagonal (top-right to bottom-left)
        for i in range(3):
            marked[i][2 - i] = True
        assert count_diagonals(marked) == 1
    
    def test_count_diagonals_square_both(self):
        """Test square card with both diagonals complete."""
        marked = [[True] * 3 for _ in range(3)]
        assert count_diagonals(marked) == 2
    
    def test_count_diagonals_5x5(self):
        """Test with 5x5 square card."""
        marked = [[False] * 5 for _ in range(5)]
        # Mark main diagonal
        for i in range(5):
            marked[i][i] = True
        assert count_diagonals(marked) == 1
    
    def test_count_diagonals_partial_diagonal(self):
        """Test that partial diagonal doesn't count."""
        marked = [[False] * 3 for _ in range(3)]
        # Mark only 2 of 3 diagonal positions
        marked[0][0] = True
        marked[1][1] = True
        # Last position not marked
        assert count_diagonals(marked) == 0
