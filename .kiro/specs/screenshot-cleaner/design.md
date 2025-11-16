# Design Document

## Overview

The Screenshot Cleaner is a Python CLI application built using the Python Fire framework for automatic command-line interface generation and Rich for enhanced console output. The tool follows a modular architecture with clear separation between OS utilities, file discovery, deletion logic, logging, and CLI interface layers.

The application will be packaged as a standard Python project managed by uv, with a single entry point command `screenshots-cleaner` that provides two subcommands: `preview` and `clean`. The tool includes comprehensive unit tests suitable for open-source distribution and documentation for configuring macOS to run the cleaner automatically at startup.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI Layer                            │
│                    (Python Fire + Rich)                      │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │  preview command │         │  clean command   │         │
│  └──────────────────┘         └──────────────────┘         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Core Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Platform    │  │   Scanner    │  │   Cleanup    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Utils Layer                             │
│                   (Logging: stdout + file)                   │
└─────────────────────────────────────────────────────────────┘
```

### Module Structure

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
```

**Module Organization:**
- **cli.py**: Top-level CLI interface using Python Fire
- **core/**: Core business logic
  - **scanner.py**: Screenshot discovery, pattern matching, age filtering
  - **cleanup.py**: File deletion with dry-run support
  - **platform.py**: macOS detection and validation
- **utils/**: Supporting utilities
  - **logging.py**: Logging configuration and output formatting

## Components and Interfaces

### 1. Platform Module (`core/platform.py`)

**Purpose:** Detect and validate the operating system.

**Interface:**
```python
def is_macos() -> bool:
    """Check if the current platform is macOS."""
    
def validate_macos() -> None:
    """Raise SystemExit if not running on macOS."""
```

**Implementation Notes:**
- Use `platform.system()` to detect OS
- Return `True` only when platform is "Darwin"
- `validate_macos()` should be called at CLI entry point

### 2. Scanner Module (`core/scanner.py`)

**Purpose:** Discover and filter screenshot files based on age and naming patterns.

**Interface:**
```python
def get_default_screenshot_dir() -> Path:
    """Get the default macOS screenshot directory (typically ~/Desktop)."""

def matches_screenshot_pattern(filename: str) -> bool:
    """Check if filename matches common screenshot patterns."""

def get_file_age_days(file_path: Path) -> int:
    """Calculate file age in days based on modification time."""

def find_expired_files(
    directory: Path,
    days: int = 7
) -> list[Path]:
    """Find all expired screenshot files in the directory."""
```

**Implementation Notes:**
- Screenshot patterns to match:
  - `Screen Shot *.png`
  - `Screenshot *.png`
  - Case-insensitive matching
- Use `os.path.getmtime()` for file age calculation
- Only scan files in the target directory (no subdirectory traversal)
- Return empty list if directory doesn't exist or is inaccessible

### 3. Cleanup Module (`core/cleanup.py`)

**Purpose:** Handle file deletion with dry-run support.

**Interface:**
```python
def delete_file(file_path: Path, dry_run: bool = False) -> bool:
    """Delete a single file. Returns True if successful (or would be in dry-run)."""

def delete_files(
    files: list[Path],
    dry_run: bool = False,
    logger: Logger = None
) -> tuple[int, int]:
    """Delete multiple files. Returns (success_count, failure_count)."""
```

**Implementation Notes:**
- In dry-run mode, log what would be deleted but don't perform deletion
- Use `os.remove()` for actual deletion
- Catch and log exceptions for individual file failures
- Never delete files outside the originally specified directory
- Return success/failure counts for reporting

### 4. Logging Module (`utils/logging.py`)

**Purpose:** Provide structured logging to stdout and optional file output.

**Interface:**
```python
def setup_logger(log_file: Path | None = None) -> Logger:
    """Configure and return a logger instance."""

def log_info(message: str) -> None:
    """Log an info-level message."""

def log_error(message: str) -> None:
    """Log an error-level message."""

def log_file_operation(file_path: Path, operation: str, success: bool) -> None:
    """Log a file operation with status."""
```

**Implementation Notes:**
- Use Python's built-in `logging` module
- Format: `[TIMESTAMP] LEVEL: message`
- Always output to stdout
- If log_file is specified, also write to file
- Use Rich console for colorized stdout output

### 5. CLI Module (`cli.py`)

**Purpose:** Provide the command-line interface using Python Fire.

**Interface:**
```python
class ScreenshotCleaner:
    """CLI for cleaning up old screenshot files."""
    
    def preview(
        self,
        path: str | None = None,
        days: int = 7,
        log_file: str | None = None
    ) -> None:
        """Preview screenshots that would be deleted.
        
        Args:
            path: Screenshot directory (default: system screenshot location)
            days: Age threshold in days (default: 7)
            log_file: Optional log file path
        """
    
    def clean(
        self,
        path: str | None = None,
        days: int = 7,
        force: bool = False,
        dry_run: bool = False,
        log_file: str | None = None
    ) -> None:
        """Delete old screenshots.
        
        Args:
            path: Screenshot directory (default: system screenshot location)
            days: Age threshold in days (default: 7)
            force: Skip confirmation prompt
            dry_run: Preview only, don't delete
            log_file: Optional log file path
        """

def main():
    """Entry point for the CLI."""
    fire.Fire(ScreenshotCleaner)
```

**Implementation Notes:**
- Python Fire automatically generates CLI from class methods
- Call `validate_macos()` at the start of each command
- If `path` not provided, use `get_default_screenshot_dir()`
- For `preview`: always run in dry-run mode, display file list and count
- For `clean`: prompt for confirmation unless `force=True`
- Use Rich tables to display file lists
- Exit with code 0 on success, non-zero on error
- Fire handles `--help` automatically from docstrings

## Data Models

### File Information

The application works primarily with `pathlib.Path` objects. No complex data models are needed, but we track:

```python
# Implicit structure used throughout
FileInfo = {
    "path": Path,           # Full file path
    "age_days": int,        # Age in days
    "size_bytes": int       # File size (for reporting)
}
```

### Operation Result

```python
# Returned from deletion operations
OperationResult = {
    "success_count": int,
    "failure_count": int,
    "files_processed": list[Path]
}
```

## Error Handling

### Platform Validation
- Check OS at startup
- Exit with clear error message if not macOS
- Exit code: 1

### Directory Access
- Validate directory exists before scanning
- Handle permission errors gracefully
- Log error and exit with code 2

### File Deletion Errors
- Catch exceptions per file (don't fail entire batch)
- Log each failure with reason
- Continue processing remaining files
- Report summary at end

### Invalid Arguments
- Python Fire handles basic type conversion
- Custom validation for:
  - Days must be positive integer
  - Path must be a directory if provided
- Exit code: 3 for invalid arguments

## Testing Strategy

### Unit Testing Approach

The project will include comprehensive unit tests suitable for open-source distribution. Tests will use pytest as the testing framework with pytest-cov for coverage reporting.

**Test Structure:**
```
tests/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── test_platform.py
│   ├── test_scanner.py
│   └── test_cleanup.py
├── utils/
│   ├── __init__.py
│   └── test_logging.py
├── test_cli.py
└── conftest.py          # Shared fixtures
```

**Test Modules:**

**1. `test_platform.py` - OS detection logic**
- Mock `platform.system()` to return "Darwin" and other values
- Verify `is_macos()` returns correct boolean
- Verify `validate_macos()` raises SystemExit on non-macOS
- Test edge cases and error conditions

**2. `test_scanner.py` - File discovery and filtering**
- Test screenshot pattern matching with various filenames:
  - Valid: "Screen Shot 2024-01-01 at 10.00.00 AM.png"
  - Valid: "Screenshot 2024-01-01.png"
  - Invalid: "document.png", "photo.jpg"
- Test age calculation with mocked file timestamps
- Test `find_expired_files()` with temporary test files
- Verify no subdirectory traversal
- Test empty directory handling
- Test permission error handling

**3. `test_cleanup.py` - Deletion logic with dry-run**
- Test dry-run mode doesn't delete files
- Test actual deletion with temporary files
- Test error handling for permission errors
- Verify success/failure counting
- Test batch deletion with mixed success/failure
- Test that files outside target directory are never deleted

**4. `test_logging.py` - Logging output**
- Verify stdout output format
- Verify file output when log_file specified
- Test log levels and formatting
- Test timestamp formatting
- Test concurrent logging operations

**5. `test_cli.py` - CLI interface**
- Test `preview` command with various arguments
- Test `clean` command with force flag
- Test `clean` command with dry-run flag
- Test confirmation prompt behavior
- Test error handling and exit codes
- Mock user input for confirmation tests
- Test integration with Fire framework

**Test Coverage Goals:**
- Minimum 90% code coverage
- 100% coverage for critical paths (deletion logic, path validation)
- All error conditions tested
- All command-line argument combinations tested

**Testing Tools:**
- pytest: Test framework
- pytest-cov: Coverage reporting
- pytest-mock: Mocking utilities
- pytest-tmp-path: Temporary file fixtures

### Integration Testing

**Manual Testing Scenarios:**
1. Create test directory with dummy screenshot files of various ages
2. Run `preview` command and verify output
3. Run `clean --dry-run` and verify no deletion
4. Run `clean` with confirmation and verify deletion
5. Run `clean --force` and verify immediate deletion
6. Test with custom `--path` and `--days` values
7. Test `--log-file` output
8. Verify behavior on non-macOS (if possible)

### UV Installation Testing

**Validation Steps:**
1. Test `uv run screenshots-cleaner preview` from project directory
2. Test `uv tool install .` for global installation
3. Verify global command `screenshots-cleaner` works after installation
4. Test uninstall with `uv tool uninstall screenshots-cleaner`

## Performance Considerations

### File Scanning Optimization
- Use `os.scandir()` for efficient directory listing
- Filter by pattern before checking file age
- Avoid unnecessary stat calls
- Target: <2 seconds for directories with <10k files

### Memory Management
- Process files in single pass (no multiple directory scans)
- Don't load file contents into memory
- Use generators where appropriate for large file lists

## Security Considerations

### Path Safety
- Validate that target directory is absolute path
- Never follow symlinks outside target directory
- Prevent path traversal attacks
- Only delete files directly in target directory (no recursion)

### Pattern Matching Safety
- Use strict pattern matching (no wildcards from user input)
- Hardcode screenshot patterns in code
- Prevent accidental deletion of non-screenshot files

## Future Extensibility

The design supports future enhancements:

1. **Archive Mode**: Add `--archive` flag to move files instead of deleting
2. **Cloud Backup**: Add `--backup-s3` to upload before deletion
3. **Scheduling**: Generate launchd plist for automated runs
4. **Custom Patterns**: Allow user-defined filename patterns
5. **Recursive Mode**: Add `--recursive` flag for subdirectory scanning
6. **Size Filtering**: Add `--min-size` and `--max-size` filters

These can be added without major architectural changes due to the modular design.

## macOS Startup Automation

### LaunchAgent Configuration

To run the Screenshot Cleaner automatically at startup or on a schedule, macOS provides the `launchd` system. The tool will include documentation and a helper script to generate the necessary configuration.

**LaunchAgent Plist Location:**
```
~/Library/LaunchAgents/com.screenshotcleaner.plist
```

**Example Plist Configuration:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.screenshotcleaner</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/Users/USERNAME/.local/bin/screenshots-cleaner</string>
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

**Configuration Options:**

1. **Run at Startup:**
```xml
<key>RunAtLoad</key>
<true/>
```

2. **Run on Schedule (Daily at 9 AM):**
```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>9</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>
```

3. **Run on Interval (Every 6 hours):**
```xml
<key>StartInterval</key>
<integer>21600</integer>
```

**Setup Instructions (to be documented in README):**

1. Install the tool globally:
   ```bash
   uv tool install screenshots-cleaner
   ```

2. Find the installation path:
   ```bash
   which screenshots-cleaner
   ```

3. Create the plist file at `~/Library/LaunchAgents/com.screenshotcleaner.plist`

4. Update the `ProgramArguments` path to match your installation

5. Load the LaunchAgent:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.screenshotcleaner.plist
   ```

6. Verify it's loaded:
   ```bash
   launchctl list | grep screenshotcleaner
   ```

7. To unload:
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.screenshotcleaner.plist
   ```

**Helper Script (Optional Enhancement):**

A future enhancement could include a `setup-autorun` command that generates and installs the plist file automatically:

```python
def setup_autorun(
    self,
    schedule: str = "daily",
    hour: int = 9,
    days: int = 7
) -> None:
    """Generate and install LaunchAgent for automatic execution.
    
    Args:
        schedule: 'startup', 'daily', or 'interval'
        hour: Hour to run (0-23) for daily schedule
        days: Age threshold for cleanup
    """
```

This would be implemented as an additional method in the `ScreenshotCleaner` class.
