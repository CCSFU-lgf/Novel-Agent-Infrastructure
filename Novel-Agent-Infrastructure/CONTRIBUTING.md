# Contributing to Novel Agent Infrastructure

Thank you for your interest in contributing to Novel Agent Infrastructure! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project follows the Contributor Covenant Code of Conduct. By participating, you are expected to uphold this code.

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a new branch
4. Make your changes
5. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- pip or poetry

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/novel-agent/novel-agent-infrastructure.git
cd novel-agent-infrastructure

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
make install-dev

# Run tests to verify setup
make test
```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-new-platform`
- `fix/memory-engine-bug`
- `docs/update-readme`
- `refactor/agent-system`

### Commit Messages

Write clear, descriptive commit messages:

```
feat: add Wattpad platform adapter

- Implement WattpadPlatform class
- Add title validation
- Add genre and tag support
- Add market analysis

Closes #123
```

Use conventional commits:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `style:` for formatting
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
pytest tests/unit/test_platform.py

# Run with coverage
pytest --cov=novel_agent --cov-report=html

# Run specific test
pytest tests/unit/test_platform.py::TestPlatform::test_validate_title
```

### Writing Tests

1. Create test files in `tests/`
2. Use pytest fixtures for common setup
3. Test both success and error cases
4. Aim for high coverage

Example:

```python
import pytest
from novel_agent.core.platform import Platform, PlatformType

class TestPlatform:
    def test_validate_title_valid(self):
        platform = Platform.create(PlatformType.ROYALROAD)
        result = platform.validate_title("Valid Title")
        assert result.is_valid is True

    def test_validate_title_too_short(self):
        platform = Platform.create(PlatformType.ROYALROAD)
        result = platform.validate_title("A")
        assert result.is_valid is False
```

## Code Style

### Formatting

We use:
- **Black** for code formatting
- **isort** for import sorting
- **Ruff** for linting
- **mypy** for type checking

Run all checks:

```bash
make format  # Format code
make lint    # Check style
make type-check  # Type checking
```

### Guidelines

1. Follow PEP 8
2. Use type annotations
3. Write docstrings (Google style)
4. Keep functions focused
5. Use meaningful names

Example:

```python
def validate_title(title: str, platform: str = "royalroad") -> TitleValidationResult:
    """Validate a story title for a specific platform.

    Args:
        title: The title to validate
        platform: Target platform name

    Returns:
        TitleValidationResult with validation details

    Raises:
        ValueError: If platform is not supported
    """
    # Implementation
```

## Submitting Changes

### Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit PR with clear description

### PR Description

Use the PR template and include:
- What changes were made
- Why changes were made
- How to test changes
- Related issues

## Reporting Issues

### Bug Reports

Use the bug report template and include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details

### Feature Requests

Use the feature request template and include:
- Problem description
- Proposed solution
- Alternatives considered

## Getting Help

- **GitHub Issues**: For bugs and features
- **Discord**: For questions and discussion
- **Email**: team@novel-agent.dev

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Invited to join the team (for significant contributions)

Thank you for contributing! 🎉
