# Screenshot Cleaner

A Python CLI tool for automatically cleaning up old macOS screenshots. Keep your Desktop tidy by automatically deleting screenshots older than a specified number of days.

## Features

- 🍎 **macOS Native**: Designed specifically for macOS screenshot patterns
- 🔍 **Smart Detection**: Automatically finds screenshots by filename pattern
- 🛡️ **Safe Operation**: Preview mode and confirmation prompts prevent accidental deletion
- 📊 **Rich Output**: Beautiful tables and colorized console output
- 📝 **Logging**: Optional file logging for audit trails
- ⚡ **Fast**: Efficiently scans directories with thousands of files

## Installation

### Using uv (Recommended)

Install globally using uv:

```bash
uv tool install screenshots-cleaner
```

Or run directly from the project directory:

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
screenshots-cleaner preview

# Preview with custom age threshold
screenshots-cleaner preview --days=14

# Preview in a specific directory
screenshots-cleaner preview --path=/path/to/screenshots

# Save log to file
screenshots-cleaner preview --log-file=preview.log
```

### Clean Mode

Delete old screenshots:

```bash
# Clean with confirmation prompt
screenshots-cleaner clean

# Clean without confirmation (use with caution!)
screenshots-cleaner clean --force

# Dry run (preview without deleting)
screenshots-cleaner clean --dry-run

# Custom age threshold
screenshots-cleaner clean --days=30

# Custom directory
screenshots-cleaner clean --path=/path/to/screenshots

# With logging
screenshots-cleaner clean --force --log-file=cleanup.log
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
   uv tool install screenshots-cleaner
   ```

2. Find the installation path:
   ```bash
   which screenshots-cleaner
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
        <string>/Users/YOUR_USERNAME/.local/bin/screenshots-cleaner</string>
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
uv run pytest --cov=screenshots_cleaner --cov-report=html
```

### Project Structure

```
screenshots_cleaner/
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
uv run pytest --cov=screenshots_cleaner --cov-report=html
open htmlcov/index.html
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Guidelines

1. Write tests for new features
2. Maintain test coverage above 90%
3. Follow existing code style
4. Update documentation as needed
5. Add type hints to all functions

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

## Acknowledgments

Built with:
- [Python Fire](https://github.com/google/python-fire) - CLI framework
- [Rich](https://github.com/Textualize/rich) - Terminal formatting
- [uv](https://github.com/astral-sh/uv) - Python package manager
