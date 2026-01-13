# Contributing to fwen

Thank you for your interest in contributing to fwen! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Getting Help](#getting-help)

## Code of Conduct

Please read and follow our [Code of Conduct](.github/CODE_OF_CONDUCT.md).

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Flutter 3.22.0 or higher
- Dart 3.4.0 or higher
- uv (recommended) or pip

### Setting Up Development Environment

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/yourusername/fwen.git
   cd fwen
   ```

2. **Install uv (recommended):**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Create a virtual environment and install dependencies:**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e ".[dev]"
   ```

4. **Run tests to verify setup:**
   ```bash
   uv run pytest
   ```

## Development Workflow

### 1. Branch Naming

Create a branch for your contribution:
```bash
git checkout -b feat/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Making Changes

- Write clear, concise commit messages
- Follow the commit message convention:
  - `feat:` - New feature
  - `fix:` - Bug fix
  - `docs:` - Documentation changes
  - `test:` - Adding or updating tests
  - `refactor:` - Code refactoring
  - `chore:` - Maintenance tasks

### 3. Running Tests

Before committing, run:
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/fwen

# Run linting
uv run ruff check .
```

### 4. Submitting a Pull Request

1. Push your branch:
   ```bash
   git push origin feat/your-feature-name
   ```

2. Create a pull request on GitHub
3. Fill out the PR template
4. Wait for review and address any feedback

## Coding Standards

### Python Style

We use [ruff](https://github.com/astral-sh/ruff) for linting and formatting:

```bash
# Check code style
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

### Code Organization

- Keep functions focused and under 50 lines
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Follow PEP 8 guidelines

### Testing

- Write tests for all new functionality
- Maintain test coverage above 80%
- Use descriptive test names
- Mock external dependencies (Flutter, file system)

### Documentation

- Update README.md if changing user-facing behavior
- Add docstrings to new functions and classes
- Update CHANGELOG.md for user-visible changes

## Submitting Changes

### Pull Request Checklist

Before submitting your PR, ensure:

- [ ] All tests pass
- [ ] Code follows the style guide
- [ ] Documentation is updated
- [ ] Commit messages follow the convention
- [ ] PR description clearly describes the changes
- [ ] Related issues are referenced

### Review Process

1. Automated checks must pass (tests, linting)
2. At least one maintainer reviews your PR
3. Address any feedback or requests for changes
4. Once approved, your PR will be merged

## Getting Help

### Resources

- [Documentation](https://github.com/yourusername/fwen#readme)
- [Issue Tracker](https://github.com/calvingit/fwen/issues)
- [Discussions](https://github.com/calvingit/fwen/discussions)

### Asking Questions

- Check existing issues and discussions first
- Create a new issue with the `question` label
- Be specific and provide context
- Include code examples if applicable

### Reporting Bugs

- Use the bug report template
- Include steps to reproduce
- Provide your environment details (OS, Python version, Flutter version)
- Add logs or screenshots if applicable

---

Thank you for contributing to fwen! 🚀
