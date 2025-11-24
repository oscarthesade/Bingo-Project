"""
Pytest configuration and shared fixtures for Bingo game tests.
"""
import sys
from pathlib import Path

# Add parent directory to path so we can import from bingo-game
project_root = Path(__file__).parent.parent
bingo_game_path = project_root / "bingo-game"
sys.path.insert(0, str(bingo_game_path))

import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture
def sample_card_numbers():
    """Sample numbers for creating a test Bingo card (3x5 = 15 numbers)."""
    return [1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 20, 21, 22, 23, 24]


@pytest.fixture
def mock_redis_client():
    """Mock Redis client for testing ScoreTracker without actual Redis."""
    mock_client = MagicMock()
    mock_client.ping.return_value = True
    mock_client.get.return_value = None
    mock_client.set.return_value = True
    mock_client.lpush.return_value = 1
    return mock_client


@pytest.fixture
def empty_marked_card():
    """Empty 3x5 marked card (all False)."""
    return [[False] * 5 for _ in range(3)]


@pytest.fixture
def one_line_marked():
    """Card with one complete line marked."""
    marked = [[False] * 5 for _ in range(3)]
    # Mark first row completely
    marked[0] = [True] * 5
    return marked


@pytest.fixture
def all_lines_marked():
    """Card with all 3 lines marked (BINGO)."""
    return [[True] * 5 for _ in range(3)]


@pytest.fixture
def partial_marked():
    """Card with some numbers marked but no complete lines."""
    marked = [[False] * 5 for _ in range(3)]
    # Mark some random positions
    marked[0][0] = True
    marked[0][2] = True
    marked[1][1] = True
    marked[1][3] = True
    marked[2][0] = True
    marked[2][4] = True
    return marked