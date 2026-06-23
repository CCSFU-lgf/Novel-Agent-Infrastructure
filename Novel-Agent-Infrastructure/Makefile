.PHONY: help install install-dev test lint format type-check docs clean build publish

# Default target
help:
	@echo "Novel Agent Infrastructure - Development Commands"
	@echo "=================================================="
	@echo ""
	@echo "Setup:"
	@echo "  install       Install the package"
	@echo "  install-dev   Install with development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  test          Run tests with coverage"
	@echo "  lint          Run linter (ruff)"
	@echo "  format        Format code (black + isort)"
	@echo "  type-check    Run type checker (mypy)"
	@echo "  pre-commit    Run pre-commit hooks"
	@echo ""
	@echo "Documentation:"
	@echo "  docs          Build documentation"
	@echo "  docs-serve    Serve documentation locally"
	@echo ""
	@echo "Build & Publish:"
	@echo "  build         Build the package"
	@echo "  publish       Publish to PyPI"
	@echo ""
	@echo "MCP:"
	@echo "  mcp-server    Start MCP server"
	@echo "  mcp-test      Test MCP server"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

# Testing
test:
	pytest tests/ -v --cov=novel_agent --cov-report=term-missing --cov-report=html

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

test-mcp:
	pytest tests/mcp/ -v

# Linting and Formatting
lint:
	ruff check src/ tests/

format:
	black src/ tests/
	isort src/ tests/

format-check:
	black --check src/ tests/
	isort --check-only src/ tests/

# Type Checking
type-check:
	mypy src/novel_agent/

# Pre-commit
pre-commit:
	pre-commit run --all-files

# Documentation
docs:
	mkdocs build

docs-serve:
	mkdocs serve

docs-deploy:
	mkdocs gh-deploy

# Build
build:
	python -m build

# Clean
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Publish
publish: clean build
	twine upload dist/*

publish-test: clean build
	twine upload --repository testpypi dist/*

# MCP Server
mcp-server:
	python -m novel_agent.mcp.server

mcp-test:
	python -m novel_agent.mcp.test

# Development shortcuts
dev: install-dev format lint type-check test

check: format-check lint type-check test

# Docker
docker-build:
	docker build -t novel-agent-infrastructure .

docker-run:
	docker run -it --rm novel-agent-infrastructure

docker-compose:
	docker-compose up -d

# Database
db-init:
	python -m novel_agent.db.init

db-migrate:
	alembic upgrade head

db-reset:
	alembic downgrade base
	alembic upgrade head

# Benchmarks
benchmark:
	python -m novel_agent.benchmarks.run

# Examples
example-quickstart:
	python examples/quickstart/basic_usage.py

example-mcp:
	python examples/mcp/server_example.py

example-agent:
	python examples/agents/workflow_example.py
