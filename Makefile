.PHONY: run test lint fmt install clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  run      - Start the FastAPI development server"
	@echo "  test     - Run pytest tests"
	@echo "  lint     - Run ruff linter"
	@echo "  fmt      - Format code with black and ruff"
	@echo "  install  - Install dependencies"
	@echo "  clean    - Clean up temporary files"

# Install dependencies
install:
	pip install -r requirements.txt

# Run the FastAPI development server
run:
	.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	PYTHONPATH=. .venv/bin/pytest -v

# Run linter
lint:
	.venv/bin/ruff check .
	.venv/bin/black --check .

# Format code
fmt:
	.venv/bin/black .
	.venv/bin/ruff check --fix .

# Clean up temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
