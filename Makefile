.PHONY: help install pre-commit-install format lint test docker-up docker-down clean

help:
	@echo "Available commands:"
	@echo "  make install            - Install dependencies"
	@echo "  make pre-commit-install - Install pre-commit hooks"
	@echo "  make format             - Format code with black and isort"
	@echo "  make lint               - Run linters (ruff, mypy)"
	@echo "  make test               - Run tests"
	@echo "  make docker-up          - Start Docker containers"
	@echo "  make docker-down        - Stop Docker containers"
	@echo "  make clean              - Clean cache files"

install:
	pip install -r requirements.txt

pre-commit-install: install
	pre-commit install
	@echo "✓ Pre-commit hooks installed successfully!"

format:
	black src/ tests/
	isort src/ tests/
	@echo "✓ Code formatted!"

lint:
	ruff check src/ tests/
	mypy src/
	@echo "✓ Linting complete!"

test:
	pytest

docker-up:
	docker-compose up --build -d
	@echo "✓ Docker containers started!"
	@echo "  API: http://localhost:8000"
	@echo "  Docs: http://localhost:8000/docs"

docker-down:
	docker-compose down
	@echo "✓ Docker containers stopped!"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	@echo "✓ Cleaned cache files!"
