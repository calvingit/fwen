# AGENTS.md

This file provides context and rules for AI coding agents working on the fwen project.

## Project Overview

**Name:** fwen
**Purpose:** Flutter Clean Architecture scaffolder CLI tool
**Language:** Python 3.11+
**Package Manager:** uv

## Repository Structure

```
fwen/
├── src/fwen/              # Main package source code
│   ├── __init__.py      # Package exports
│   ├── __main__.py      # CLI entry point (enables: python -m fwen)
│   ├── actions.py       # Post-creation actions menu
│   ├── cli.py           # Command-line argument parser
│   ├── config.py        # Configuration management and validation
│   ├── generator.py     # Project generation logic
│   ├── prompts.py       # Interactive prompt definitions
│   └── utils.py         # Helper functions
├── tests/                # Test suite
│   ├── test_config.py
│   ├── test_generator.py
│   ├── test_utils.py
│   └── run_tests.py      # Test runner
├── templates/            # Flutter project templates
│   ├── base/            # Core templates always included
│   ├── state_management/  # Bloc, Provider, Riverpod templates
│   └── navigation/      # GoRouter, AutoRoute, Navigator templates
├── scripts/             # Helper scripts
│   ├── feature-dev.py   # Feature generator
│   └── install_dependencies.sh
├── .github/workflows/   # CI/CD pipelines
├── pyproject.toml       # Python packaging configuration
└── .python-version      # Python version pin for uv
```

## Coding Rules

### Python Standards
- **Style:** Follow ruff linting (line length: 100)
- **Type Hints:** Required for all function parameters and returns
- **Docstrings:** Google-style docstrings for all public functions/classes
- **Imports:** Use `isort` ordering (via ruff)

### Code Organization
- Keep functions under 50 lines when possible
- One class per file unless tightly related
- Use descriptive names (no abbreviations)
- Avoid deeply nested code (max 4 levels)

### Error Handling
- Use specific exception types
- Include helpful error messages
- Log errors before raising
- Validate all external inputs

## Development Commands

### Installation
```bash
uv pip install -e ".[dev]"
```

### Running Tests
```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=src/fwen

# Specific test file
uv run pytest tests/test_config.py
```

### Linting
```bash
# Check code
uv run ruff check .

# Auto-fix
uv run ruff check --fix .

# Format code
uv run ruff format .
```

### Running the CLI
```bash
# Interactive mode
uv run fwen

# Non-interactive mode
uv run fwen --project-name test_app --org com.example --yes

# Or via module
python -m fwen
```

## File-Specific Rules

### `src/fwen/cli.py`
- Uses argparse for argument parsing
- All prompt options must have matching arguments
- Validation must happen before project generation

### `src/fwen/config.py`
- All default values defined in `DEFAULTS` constant
- Validation functions return `(is_valid, error_message)` tuples
- Case conversion functions for project names

### `src/fwen/generator.py`
- Creates output directory if it doesn't exist
- Only sets `project_path` after successful Flutter creation
- Uses `copy_directory` for template application

### `src/fwen/prompts.py`
- Uses questionary for all interactive prompts
- One section per async method
- Progress indicator shows `[section/total]`

### `src/fwen/templates/`
- Use `{{variable}}` substitution pattern
- Base templates always applied
- Feature-specific templates conditional on config

## Release Process

### Version Bump
1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` with new section
3. Commit changes

### Tag and Release
```bash
git tag -a v0.x.x -m "Release v0.x.x"
git push origin v0.x.x
```

GitHub Actions will automatically:
- Run tests
- Build package
- Publish to PyPI

## Repository-Specific Information

### Placeholder Values to Update
- `calvingit` - GitHub username
- `calvingit@users.noreply.github.com` - Email for PyPI

### Key Dependencies
- `questionary>=2.0` - Interactive prompts
- `rich>=14.0` - Terminal formatting
- `pyyaml>=6.0` - YAML parsing

### Generated Project Structure
```
lib/
├── bootstrap.dart
├── main.dart
├── app/ (config, router)
├── core/ (di, network, services, blocs/usecases)
├── features/ (feature modules)
└── shared/ (widgets, themes, models)
```

## Important Notes for Agents

1. **Template System:** Templates use `{{variable}}` substitution. Keys are generated from `config.get_substitution_vars()`.

2. **Flutter Command:** Always use `get_flutter_executable()` from utils.py to get the Flutter path.

3. **Path Handling:** All paths use `pathlib.Path`. Never use string concatenation for paths.

4. **Async Functions:** All prompt and action functions are async. Use `asyncio.run()` to execute.

5. **Module Imports:** When importing from `fwen`, use absolute imports: `from fwen.config import Config`.

6. **Testing:** Tests use `unittest` and `unittest.mock`. Do not use third-party test frameworks.

7. **Python Version:** Pin to 3.11 in `.python-version`. Support 3.11-3.13 in CI.

8. **Package Entry Point:** `src/fwen/__main__.py` enables both `python -m fwen` and `fwen` commands.

9. **Templates Directory:** Located at project root (not inside `src/`). Path is `Path(__file__).parent.parent.parent / "templates"`.

10. **Non-Interactive Mode:** Skip post-creation menu, just print next steps instead.

## Common Tasks

### Add a new CLI argument
1. Add argument to `create_parser()` in `cli.py`
2. Add validation in `validate_args()`
3. Add to `args_to_config()` mapping
4. Update `README.md` documentation

### Add a new template
1. Create directory in `templates/`
2. Add template files with `{{variable}}` substitutions
3. Reference in `generator._apply_templates()`

### Add a new state management option
1. Create `templates/state_management/<name>/`
2. Add base files
3. Update `config.STATE_MANAGEMENT_OPTIONS`
4. Update `cli.py` argument choices
5. Update `config.get_pubspec_dependencies()`

### Fix a bug
1. Write test that reproduces the bug
2. Fix the code
3. Verify test passes
4. Update CHANGELOG.md if user-facing

## Testing Checklist

Before submitting:
- [ ] All tests pass: `uv run pytest`
- [ ] No linting errors: `uv run ruff check .`
- [ ] Code formatted: `uv run ruff format .`
- [ ] Documentation updated (README or docs/)
- [ ] CHANGELOG.md updated (if applicable)
