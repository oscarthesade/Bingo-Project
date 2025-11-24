# Testing Guide

## Quick Start

1. **Install test dependencies:**
   ```bash
   make install-test
   ```

2. **Run all tests:**
   ```bash
   make test
   ```

3. **Run tests with coverage:**
   ```bash
   make test-cov
   ```

## Test Files Overview

### `test_card.py` - BingoCard Tests
- ✅ Card initialization (custom and random)
- ✅ Number marking functionality
- ✅ Bingo detection (rows, columns)
- ✅ Card display/string representation
- ✅ Edge cases and error handling

### `test_check.py` - Check Module Tests
- ✅ Line counting (`count_lines`)
- ✅ Bingo detection (`is_bingo`)
- ✅ Diagonal counting (`count_diagonals`)
- ✅ Various card configurations

### `test_draw.py` - NumberDrawer Tests
- ✅ Initialization and shuffling
- ✅ Number drawing
- ✅ Drawn number tracking
- ✅ Reset functionality
- ✅ Exhaustion handling

### `test_score.py` - ScoreTracker Tests
- ✅ Score calculation
- ✅ Line completion scoring
- ✅ Bingo bonus scoring
- ✅ Redis integration (mocked)
- ✅ High score retrieval
- ✅ Error handling

## Running Specific Tests

```bash
# Run one test file
pytest tests/test_card.py

# Run one test class
pytest tests/test_card.py::TestBingoCardInitialization

# Run one specific test
pytest tests/test_card.py::TestBingoCardInitialization::test_init_with_custom_numbers

# Run with verbose output
pytest -v

# Run with print statements visible
pytest -s
```

## Coverage

View coverage report:
```bash
make test-html
open htmlcov/index.html
```

## Docker Testing

Run tests inside Docker container:
```bash
make docker-test
```

This ensures tests run in the same environment as production.

## Continuous Integration

For CI/CD pipelines:
```bash
make ci-test
```

Generates:
- Coverage XML report
- JUnit XML report
- Terminal coverage output