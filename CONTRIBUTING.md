# Contributing to Screenshot Cleaner

Thank you for your interest in contributing to Screenshot Cleaner! This document provides guidelines and instructions for contributing.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd screenshot-cleaner
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Run tests:**
   ```bash
   uv run pytest
   ```

## Development Workflow

### Making Changes

1. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following our coding standards

3. Write tests for your changes

4. Run the test suite:
   ```bash
   uv run pytest --cov=screenshot_cleaner
   ```

5. Ensure coverage stays above 90%

### Code Standards

- **Type Hints**: Add type hints to all function signatures
- **Docstrings**: Document all public functions and classes
- **Testing**: Write unit tests for new functionality
- **Code Style**: Follow existing code patterns
- **Imports**: Keep imports organized (stdlib, third-party, local)

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=screenshot_cleaner --cov-report=html

# Run specific test file
uv run pytest tests/core/test_scanner.py

# Run with verbose output
uv run pytest -v
```

### Testing Guidelines

1. Write tests before or alongside your code
2. Test both success and failure cases
3. Use descriptive test names
4. Mock external dependencies
5. Keep tests fast and isolated

## Version Management

We use [bump-my-version](https://github.com/callowayproject/bump-my-version) for semantic versioning.

### Semantic Versioning

- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features (backward compatible)
- **PATCH** (0.0.1): Bug fixes

### Bumping Versions

**Before bumping:**
1. Ensure all changes are committed
2. Run full test suite
3. Update CHANGELOG.md

**Bump commands:**
```bash
# Patch release (bug fixes)
uv run bump-my-version bump patch

# Minor release (new features)
uv run bump-my-version bump minor

# Major release (breaking changes)
uv run bump-my-version bump major
```

**Preview changes (dry-run):**
```bash
uv run bump-my-version bump patch --dry-run --verbose
```

### What Gets Updated

When you bump a version:
- `pyproject.toml` - project version
- `screenshot_cleaner/__init__.py` - package version
- `.bumpversion.toml` - current version tracking
- Git commit created automatically
- Git tag created (e.g., `v0.2.0`)

## Pull Request Process

1. **Update documentation** if you've changed functionality
2. **Update CHANGELOG.md** with your changes
3. **Ensure tests pass** and coverage is maintained
4. **Create a pull request** with a clear description
5. **Link any related issues** in the PR description

### PR Checklist

- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Code follows project style
- [ ] Type hints added
- [ ] Coverage maintained above 90%

## Commit Message Guidelines

Use clear, descriptive commit messages:

```
feat: Add support for custom screenshot patterns
fix: Handle permission errors gracefully
docs: Update installation instructions
test: Add tests for scanner module
refactor: Simplify cleanup logic
```

**Prefixes:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

## Release Process

### Automated Release (Recommended)

Use the release script:

```bash
./scripts/release.sh [patch|minor|major]
```

This will:
1. Run tests and verify coverage
2. Bump version and create tag
3. Push to GitHub
4. Trigger automatic PyPI publish via GitHub Actions

### Manual Release

1. **Prepare release:**
   - Update CHANGELOG.md with all changes
   - Ensure all tests pass
   - Review documentation

2. **Bump version:**
   ```bash
   uv run bump-my-version bump [patch|minor|major]
   ```

3. **Push changes:**
   ```bash
   git push
   git push --tags
   ```

4. **GitHub Actions automatically:**
   - Runs tests
   - Builds package
   - Publishes to PyPI
   - Creates GitHub release

### Publishing to PyPI

The project uses PyPI Trusted Publishers for secure, token-free publishing. See [docs/PUBLISHING.md](../docs/PUBLISHING.md) for detailed instructions.

**First-time setup:**
1. Configure trusted publisher on PyPI
2. Set up GitHub environment named `pypi`
3. Push a version tag to trigger publish

**Testing releases:**
- Use Test PyPI before production
- Run workflow manually with test flag
- Verify installation works

## Project Structure

```
screenshot_cleaner/
├── __init__.py          # Package initialization
├── cli.py               # CLI interface (Python Fire)
├── core/                # Core business logic
│   ├── platform.py      # OS detection
│   ├── scanner.py       # File discovery
│   └── cleanup.py       # Deletion operations
└── utils/               # Utilities
    └── logging.py       # Logging setup

tests/
├── core/                # Core module tests
├── utils/               # Utility tests
├── test_cli.py          # CLI tests
├── integration_test.py  # Integration tests
└── conftest.py          # Shared fixtures
```

## Getting Help

- **Issues**: Open an issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check README.md and code comments

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
