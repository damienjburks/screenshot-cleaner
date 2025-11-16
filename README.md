# Screenshot Cleaner

[![PyPI version](https://badge.fury.io/py/screenshot-cleaner.svg)](https://badge.fury.io/py/screenshot-cleaner)
[![CI/CD](https://github.com/damienjburks/screenshot-cleaner/actions/workflows/main.yml/badge.svg)](https://github.com/damienjburks/screenshot-cleaner/actions/workflows/main.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Built with Kiro](https://img.shields.io/badge/Built%20with-Kiro-5B4FE9)](https://kiro.ai)

A Python CLI tool for automatically cleaning up old macOS screenshots. Keep your Desktop tidy by automatically deleting screenshots older than a specified number of days.

## Features

- 🍎 **macOS Native**: Designed specifically for macOS screenshot patterns
- 🔍 **Smart Detection**: Automatically finds screenshots by filename pattern
- 🛡️ **Safe Operation**: Preview mode and confirmation prompts prevent accidental deletion
- 📊 **Rich Output**: Beautiful tables and colorized console output
- 📝 **Logging**: Optional file logging for audit trails
- ⚡ **Fast**: Efficiently scans directories with thousands of files

## Installation

### From PyPI (Recommended)

Install using pip:

```bash
pip install screenshot-cleaner
```

Or using uv:

```bash
uv tool install screenshot-cleaner
```

### From Source

Install from the repository:

```bash
git clone <repository-url>
cd screenshot-cleaner
uv sync
```

## Usage

### Preview Mode

See which screenshots would be deleted without actually deleting them:

```bash
# Preview screenshots older than 7 days (default)
screenshot-cleaner preview

# Preview with custom age threshold
screenshot-cleaner preview --days=14

# Preview in a specific directory
screenshot-cleaner preview --path=/path/to/screenshots

# Save log to file
screenshot-cleaner preview --log-file=preview.log
```

### Clean Mode

Delete old screenshots:

```bash
# Clean with confirmation prompt
screenshot-cleaner clean

# Clean without confirmation (use with caution!)
screenshot-cleaner clean --force

# Dry run (preview without deleting)
screenshot-cleaner clean --dry-run

# Custom age threshold
screenshot-cleaner clean --days=30

# Custom directory
screenshot-cleaner clean --path=/path/to/screenshots

# With logging
screenshot-cleaner clean --force --log-file=cleanup.log
```

## Command Reference

### `preview`

Preview screenshots that would be deleted.

**Arguments:**
- `--path`: Screenshot directory (default: ~/Desktop)
- `--days`: Age threshold in days (default: 7)
- `--log-file`: Optional log file path

### `clean`

Delete old screenshots.

**Arguments:**
- `--path`: Screenshot directory (default: ~/Desktop)
- `--days`: Age threshold in days (default: 7)
- `--force`: Skip confirmation prompt
- `--dry-run`: Preview only, don't delete
- `--log-file`: Optional log file path

## macOS Automation

You can configure macOS to run Screenshot Cleaner automatically using LaunchAgents.

### Setup Instructions

1. Install the tool globally:
   ```bash
   uv tool install screenshot-cleaner
   ```

2. Find the installation path:
   ```bash
   which screenshot-cleaner
   ```

3. Create a plist file at `~/Library/LaunchAgents/com.screenshotcleaner.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.screenshotcleaner</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/Users/YOUR_USERNAME/.local/bin/screenshot-cleaner</string>
        <string>clean</string>
        <string>--force</string>
        <string>--days</string>
        <string>7</string>
    </array>
    
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    
    <key>StandardOutPath</key>
    <string>/tmp/screenshot-cleaner.log</string>
    
    <key>StandardErrorPath</key>
    <string>/tmp/screenshot-cleaner.error.log</string>
</dict>
</plist>
```

4. Update the path in `ProgramArguments` to match your installation

5. Load the LaunchAgent:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.screenshotcleaner.plist
   ```

6. Verify it's loaded:
   ```bash
   launchctl list | grep screenshotcleaner
   ```

### Scheduling Options

**Run at startup:**
```xml
<key>RunAtLoad</key>
<true/>
```

**Run daily at 9 AM:**
```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>9</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>
```

**Run every 6 hours:**
```xml
<key>StartInterval</key>
<integer>21600</integer>
```

### Unload LaunchAgent

To stop automatic execution:
```bash
launchctl unload ~/Library/LaunchAgents/com.screenshotcleaner.plist
```

## Development

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd screenshot-cleaner

# Install dependencies
uv sync

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=screenshot_cleaner --cov-report=html
```

### Project Structure

```
screenshot_cleaner/
├── __init__.py
├── cli.py              # Fire CLI entry point
├── core/
│   ├── __init__.py
│   ├── scanner.py      # File discovery and filtering
│   ├── cleanup.py      # Deletion operations
│   └── platform.py     # OS detection
└── utils/
    ├── __init__.py
    └── logging.py      # Logging utilities

tests/
├── core/
│   ├── test_platform.py
│   ├── test_scanner.py
│   └── test_cleanup.py
├── utils/
│   └── test_logging.py
└── test_cli.py
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/core/test_scanner.py

# Run with verbose output
uv run pytest -v

# Generate coverage report
uv run pytest --cov=screenshot_cleaner --cov-report=html
open htmlcov/index.html
```

### Version Management

This project uses [bump-my-version](https://github.com/callowayproject/bump-my-version) for automated semantic versioning.

**Semantic Versioning:**
- `MAJOR.MINOR.PATCH` format (e.g., `0.1.0`)
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

**Bumping Versions:**

```bash
# Patch release (0.1.0 → 0.1.1)
uv run bump-my-version bump patch

# Minor release (0.1.0 → 0.2.0)
uv run bump-my-version bump minor

# Major release (0.1.0 → 1.0.0)
uv run bump-my-version bump major
```

**What happens when you bump:**
1. Version updated in `pyproject.toml`
2. Version updated in `screenshot_cleaner/__init__.py`
3. Git commit created automatically
4. Git tag created (e.g., `v0.2.0`)

**Before bumping:**
- Ensure all changes are committed
- Run tests to verify everything works
- Update CHANGELOG.md with changes

**Show current version:**
```bash
uv run bump-my-version show current_version
```

**Dry-run (preview changes):**
```bash
uv run bump-my-version bump patch --dry-run --verbose
```

### Release Workflow

**Automated Release Script:**

The easiest way to create a release:

```bash
# For bug fixes (0.1.0 → 0.1.1)
./scripts/release.sh patch

# For new features (0.1.0 → 0.2.0)
./scripts/release.sh minor

# For breaking changes (0.1.0 → 1.0.0)
./scripts/release.sh major
```

The script will:
- Run tests and verify coverage
- Show preview of version bump
- Ask for confirmation
- Bump version and create git tag
- Push changes and tags to remote

**Manual Release Process:**

1. **Make your changes** and commit them
2. **Run tests** to ensure everything works:
   ```bash
   uv run pytest --cov=screenshot_cleaner
   ```
3. **Update CHANGELOG.md** with your changes
4. **Bump the version**:
   ```bash
   # For bug fixes
   uv run bump-my-version bump patch
   
   # For new features
   uv run bump-my-version bump minor
   
   # For breaking changes
   uv run bump-my-version bump major
   ```
5. **Push changes and tags**:
   ```bash
   git push
   git push --tags
   ```

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:
- Development setup
- Code standards
- Testing guidelines
- Version management
- Pull request process
- Release workflow

### Quick Guidelines

1. Write tests for new features
2. Maintain test coverage above 90%
3. Follow existing code style
4. Update documentation as needed
5. Add type hints to all functions
6. Use semantic versioning for releases
7. Update CHANGELOG.md with your changes

See [CONTRIBUTING.md](CONTRIBUTING.md) for complete details.

## Troubleshooting

### "This tool only runs on macOS"

Screenshot Cleaner is designed specifically for macOS and will not run on other operating systems.

### No screenshots found

- Verify you're looking in the correct directory (default is ~/Desktop)
- Check that your screenshots match the expected patterns:
  - "Screen Shot *.png"
  - "Screenshot *.png"
- Try using `--path` to specify a different directory

### Permission errors

Ensure you have read/write permissions for the target directory.

## License

MIT License - see LICENSE file for details.

## Publishing

For maintainers: See [PUBLISHING.md](docs/PUBLISHING.md) for instructions on publishing to PyPI.

Quick release:
```bash
./scripts/release.sh patch  # Creates tag and triggers PyPI publish
```

## Acknowledgments

Built with:
- [Python Fire](https://github.com/google/python-fire) - CLI framework
- [Rich](https://github.com/Textualize/rich) - Terminal formatting
- [uv](https://github.com/astral-sh/uv) - Python package manager

Published to [PyPI](https://pypi.org/project/screenshot-cleaner/)
