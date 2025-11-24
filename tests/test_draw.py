"""
Comprehensive tests for NumberDrawer class.
"""
import pytest
from src.game.draw import NumberDrawer


class TestNumberDrawerInitialization:
    """Test NumberDrawer initialization."""
    
    def test_init_default_range(self):
        """Test initialization with default range (1-75)."""
        drawer = NumberDrawer()
        assert drawer.min_number == 1
        assert drawer.max_number == 75
        assert len(drawer.remaining) == 75
        # Check all numbers are unique and in valid range
        assert len(set(drawer.remaining)) == 75  # All unique
        assert all(1 <= n <= 75 for n in drawer.remaining)  # All in range
    
    def test_init_custom_range(self):
        """Test initialization with custom range."""
        drawer = NumberDrawer(min_number=10, max_number=20)
        assert drawer.min_number == 10
        assert drawer.max_number == 20
        assert len(drawer.remaining) == 11  # 10 to 20 inclusive
        assert all(10 <= n <= 20 for n in drawer.remaining)
    
    def test_init_shuffles_numbers(self):
        """Test that numbers are shuffled on initialization."""
        drawer1 = NumberDrawer()
        drawer2 = NumberDrawer()
        # Very unlikely to have same order (probability is 1/75!)
        assert drawer1.remaining != drawer2.remaining
    
    def test_init_empty_drawn_list(self):
        """Test that drawn_numbers starts empty."""
        drawer = NumberDrawer()
        assert drawer.drawn_numbers == []


class TestDrawNumber:
    """Test drawing numbers."""
    
    def test_draw_number_returns_number(self):
        """Test that draw_number returns a valid number."""
        drawer = NumberDrawer(min_number=1, max_number=10)
        number = drawer.draw_number()
        assert number is not None
        assert 1 <= number <= 10
    
    def test_draw_number_decreases_remaining(self):
        """Test that remaining count decreases after draw."""
        drawer = NumberDrawer(min_number=1, max_number=10)
        initial_count = len(drawer.remaining)
        drawer.draw_number()
        assert len(drawer.remaining) == initial_count - 1
    
    def test_draw_number_adds_to_drawn(self):
        """Test that drawn number is added to drawn_numbers list."""
        drawer = NumberDrawer(min_number=1, max_number=10)
        number = drawer.draw_number()
        assert number in drawer.drawn_numbers
        assert len(drawer.drawn_numbers) == 1
    
    def test_draw_all_numbers(self):
        """Test drawing all numbers in range."""
        drawer = NumberDrawer(min_number=1, max_number=5)
        drawn = []
        for _ in range(5):
            drawn.append(drawer.draw_number())
        
        assert len(drawn) == 5
        assert len(set(drawn)) == 5  # All unique
        assert len(drawer.remaining) == 0
        assert len(drawer.drawn_numbers) == 5
    
    def test_draw_after_exhaustion_returns_none(self):
        """Test that drawing after all numbers returns None."""
        drawer = NumberDrawer(min_number=1, max_number=3)
        # Draw all 3 numbers
        drawer.draw_number()
        drawer.draw_number()
        drawer.draw_number()
        # Next draw should return None
        assert drawer.draw_number() is None
    
    def test_draw_numbers_are_unique(self):
        """Test that all drawn numbers are unique."""
        drawer = NumberDrawer(min_number=1, max_number=10)
        drawn = []
        for _ in range(10):
            number = drawer.draw_number()
            drawn.append(number)
        
        assert len(drawn) == len(set(drawn))  # All unique


class TestGetDrawnNumbers:
    """Test get_drawn_numbers method."""
    
    def test_get_drawn_numbers_empty(self):
        """Test getting drawn numbers when none drawn."""
        drawer = NumberDrawer()
        assert drawer.get_drawn_numbers() == []
    
    def test_get_drawn_numbers_after_draws(self):
        """Test getting drawn numbers after drawing."""
        drawer = NumberDrawer(min_number=1, max_number=5)
        drawer.draw_number()
        drawer.draw_number()
        drawn = drawer.get_drawn_numbers()
        assert len(drawn) == 2
    
    def test_get_drawn_numbers_order(self):
        """Test that drawn numbers are in draw order."""
        drawer = NumberDrawer(min_number=1, max_number=5)
        first = drawer.draw_number()
        second = drawer.draw_number()
        drawn = drawer.get_drawn_numbers()
        assert drawn[0] == first
        assert drawn[1] == second


class TestReset:
    """Test reset method."""
    
    def test_reset_restores_all_numbers(self):
        """Test that reset restores all numbers to remaining."""
        drawer = NumberDrawer(min_number=1, max_number=10)
        # Draw some numbers
        drawer.draw_number()
        drawer.draw_number()
        assert len(drawer.remaining) == 8
        
        # Reset
        drawer.reset()
        assert len(drawer.remaining) == 10
        assert all(1 <= n <= 10 for n in drawer.remaining)
    
    def test_reset_clears_drawn_numbers(self):
        """Test that reset clears drawn_numbers list."""
        drawer = NumberDrawer(min_number=1, max_number=10)
        drawer.draw_number()
        drawer.draw_number()
        assert len(drawer.drawn_numbers) == 2
        
        drawer.reset()
        assert drawer.drawn_numbers == []
    
    def test_reset_reshuffles(self):
        """Test that reset reshuffles the numbers."""
        drawer = NumberDrawer(min_number=1, max_number=10)
        original_order = drawer.remaining[:]
        
        drawer.reset()
        # Very unlikely to have same order after reshuffle
        assert drawer.remaining != original_order
    
    def test_reset_allows_new_draws(self):
        """Test that after reset, can draw numbers again."""
        drawer = NumberDrawer(min_number=1, max_number=5)
        # Draw all
        for _ in range(5):
            drawer.draw_number()
        assert drawer.draw_number() is None
        
        # Reset and draw again
        drawer.reset()
        number = drawer.draw_number()
        assert number is not None
        assert 1 <= number <= 5