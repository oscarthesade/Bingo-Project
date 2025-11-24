.PHONY: help test test-unit test-cov test-html test-watch clean install-test install-deps lint format docker-build docker-up docker-down docker-test docker-logs

# Default target
help:
	@echo "Bingo Project - Makefile Commands"
	@echo "=================================="
	@echo ""
	@echo "Testing:"
	@echo "  make test          - Run all tests"
	@echo "  make test-unit     - Run unit tests only"
	@echo "  make test-cov      - Run tests with coverage report"
	@echo "  make test-html      - Generate HTML coverage report"
	@echo "  make test-watch    - Run tests in watch mode (requires pytest-watch)"
	@echo ""
	@echo "Installation:"
	@echo "  make venv         - Create virtual environment"
	@echo "  make install-deps  - Install application dependencies"
	@echo "  make install-test  - Install test dependencies"
	@echo "  make dev-setup     - Set up complete dev environment"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build   - Build Docker images"
	@echo "  make docker-up     - Start Docker containers"
	@echo "  make docker-down   - Stop Docker containers"
	@echo "  make docker-test   - Run tests inside Docker container"
	@echo "  make docker-logs   - View Docker container logs"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint          - Run linters (if configured)"
	@echo "  make format        - Format code (if configured)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean         - Remove test artifacts and cache"

# Variables - Auto-detect virtual environment
ifeq ($(VIRTUAL_ENV),)
  ifneq ($(wildcard .venv/bin/python),)
    VENV_PYTHON := .venv/bin/python
    VENV_PIP := .venv/bin/pip
  else ifneq ($(wildcard venv/bin/python),)
    VENV_PYTHON := venv/bin/python
    VENV_PIP := venv/bin/pip
  else
    VENV_PYTHON := python3
    VENV_PIP := pip3
  endif
else
  VENV_PYTHON := $(VIRTUAL_ENV)/bin/python
  VENV_PIP := $(VIRTUAL_ENV)/bin/pip
endif

PYTHON := $(VENV_PYTHON)
PIP := $(VENV_PIP)
TEST_DIR := tests
COV_DIR := htmlcov

# Virtual environment setup
venv:
	@echo "Creating virtual environment..."
	python3 -m venv .venv
	@echo "Virtual environment created. Activate with: source .venv/bin/activate"

# Installation
install-deps: check-venv
	@echo "Installing application dependencies..."
	$(PIP) install -r bingo-game/requirements.txt

install-test: check-venv
	@echo "Installing test dependencies..."
	$(PIP) install -r tests/requirements.txt

check-venv:
	@if [ -z "$(VIRTUAL_ENV)" ] && [ ! -f .venv/bin/python ] && [ ! -f venv/bin/python ]; then \
		echo "⚠️  No virtual environment detected!"; \
		echo "Run 'make venv' to create one, or activate your existing venv."; \
		exit 1; \
	fi

# Testing
test:
	@echo "Running all tests..."
	$(PYTHON) -m pytest $(TEST_DIR) -v

test-unit:
	@echo "Running unit tests..."
	$(PYTHON) -m pytest $(TEST_DIR) -v -m "unit or not integration"

test-cov:
	@echo "Running tests with coverage..."
	$(PYTHON) -m pytest $(TEST_DIR) --cov=bingo-game/src --cov-report=term-missing --cov-report=html

test-html:
	@echo "Generating HTML coverage report..."
	$(PYTHON) -m pytest $(TEST_DIR) --cov=bingo-game/src --cov-report=html
	@echo "Coverage report generated in $(COV_DIR)/index.html"

test-watch:
	@echo "Running tests in watch mode..."
	$(PYTHON) -m pytest $(TEST_DIR) --watch

# Docker commands
docker-build:
	@echo "Building Docker images..."
	docker compose build

docker-up:
	@echo "Starting Docker containers..."
	docker compose up -d

docker-down:
	@echo "Stopping Docker containers..."
	docker compose down

docker-test:
	@echo "Running tests in Docker container..."
	docker compose exec bingo-game python -m pytest /app/tests -v || \
	docker compose run --rm bingo-game python -m pytest /app/tests -v

docker-logs:
	@echo "Viewing Docker logs..."
	docker compose logs -f

# Code quality (placeholder - add tools as needed)
lint:
	@echo "Running linters..."
	@echo "Add your linter commands here (e.g., flake8, pylint, mypy)"

format:
	@echo "Formatting code..."
	@echo "Add your formatter commands here (e.g., black, autopep8)"

# Cleanup
clean:
	@echo "Cleaning test artifacts..."
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf $(COV_DIR)
	rm -rf htmlcov
	rm -rf coverage.xml
	rm -rf *.pyc
	rm -rf __pycache__
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete!"

# Development workflow
dev-setup: venv install-deps install-test
	@echo ""
	@echo "✅ Development environment setup complete!"
	@echo "Activate your virtual environment with: source .venv/bin/activate"

# CI/CD friendly test command
ci-test:
	@echo "Running CI tests..."
	$(PYTHON) -m pytest $(TEST_DIR) --cov=bingo-game/src --cov-report=xml --cov-report=term --junit-xml=junit.xml -v