# Bingo Project Test Suite

Comprehensive test suite for the Bingo game project using pytest.

## Test Structure

```
tests/
├── conftest.py          # Pytest configuration and shared fixtures
├── test_card.py         # Tests for BingoCard class
├── test_check.py        # Tests for check module functions
├── test_draw.py         # Tests for NumberDrawer class
├── test_score.py        # Tests for ScoreTracker class
└── requirements.txt     # Test dependencies
```

## Installation

Install test dependencies:

```bash
make install-test
# or
pip install -r tests/requirements.txt
```

## Running Tests

### Run all tests:
```bash
make test
# or
pytest
```

### Run with coverage:
```bash
make test-cov
# or
pytest --cov=bingo-game/src --cov-report=term-missing
```

### Run specific test file:
```bash
pytest tests/test_card.py
```

### Run specific test:
```bash
pytest tests/test_card.py::TestBingoCardInitialization::test_init_with_custom_numbers
```

### Run tests in Docker:
```bash
make docker-test
```

## Test Coverage

The test suite covers:

- **Card Module**: Initialization, marking, bingo detection, display
- **Check Module**: Line counting, bingo detection, diagonal counting
- **Draw Module**: Number drawing, shuffling, reset functionality
- **Score Module**: Score calculation, Redis integration (mocked), high scores

## Test Categories

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions (when applicable)

## Fixtures

Shared fixtures in `conftest.py`:
- `sample_card_numbers`: Predefined card numbers for testing
- `mock_redis_client`: Mock Redis client for ScoreTracker tests
- `empty_marked_card`: Empty marked card
- `one_line_marked`: Card with one complete line
- `all_lines_marked`: Card with all lines marked (BINGO)
- `partial_marked`: Card with partial marking

## Best Practices

1. **Isolation**: Each test is independent and can run in any order
2. **Mocking**: External dependencies (Redis) are mocked
3. **Fixtures**: Shared test data is provided via fixtures
4. **Clear Names**: Test names describe what they test
5. **Coverage**: Aim for high code coverage

## Coverage Reports

Generate HTML coverage report:
```bash
make test-html
```

View report:
```bash
open htmlcov/index.html
```