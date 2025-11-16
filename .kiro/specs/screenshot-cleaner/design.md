# Design Document

## Overview

The Screenshot Cleaner is a Python CLI application built using the Python Fire framework for automatic command-line interface generation and Rich for enhanced console output. The tool follows a modular architecture with clear separation between OS utilities, file discovery, deletion logic, logging, and CLI interface layers.

The application will be packaged as a standard Python project managed by uv, with a single entry point command `screenshot-cleaner` that provides two subcommands: `preview` and `clean`. The tool includes comprehensive unit tests suitable for open-source distribution and documentation for configuring macOS to run the cleaner automatically at startup.

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
1. Test `uv run screenshot-cleaner preview` from project directory
2. Test `uv tool install .` for global installation
3. Verify global command `screenshot-cleaner` works after installation
4. Test uninstall with `uv tool uninstall screenshot-cleaner`

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
        <string>/Users/USERNAME/.local/bin/screenshot-cleaner</string>
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
   uv tool install screenshot-cleaner
   ```

2. Find the installation path:
   ```bash
   which screenshot-cleaner
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


## Version Management

### Automated Version Control with bump-my-version

The project uses `bump-my-version` (formerly `bump2version`) for automated semantic versioning. This ensures consistent version numbers across all project files and simplifies the release process.

**Version Format:**
- Semantic versioning: `MAJOR.MINOR.PATCH`
- Example: `0.1.0` → `0.2.0` (minor bump)

**Configuration File:**
`.bumpversion.toml` contains:
- Current version
- Files to update (pyproject.toml, __init__.py)
- Commit and tag settings
- Version part definitions

**Workflow:**

1. **Patch Release** (bug fixes):
   ```bash
   bump-my-version bump patch
   # 0.1.0 → 0.1.1
   ```

2. **Minor Release** (new features, backward compatible):
   ```bash
   bump-my-version bump minor
   # 0.1.0 → 0.2.0
   ```

3. **Major Release** (breaking changes):
   ```bash
   bump-my-version bump major
   # 0.1.0 → 1.0.0
   ```

**Automated Updates:**
When bumping version, the tool automatically:
- Updates version in `pyproject.toml`
- Updates version in `screenshot_cleaner/__init__.py`
- Creates a git commit with the version change
- Creates a git tag (e.g., `v0.2.0`)

**Configuration Example:**

```toml
[tool.bumpversion]
current_version = "0.1.0"
parse = "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)"
serialize = ["{major}.{minor}.{patch}"]
search = "{current_version}"
replace = "{new_version}"
regex = false
ignore_missing_version = false
tag = true
sign_tags = false
tag_name = "v{new_version}"
tag_message = "Bump version: {current_version} → {new_version}"
allow_dirty = false
commit = true
message = "Bump version: {current_version} → {new_version}"
commit_args = ""

[[tool.bumpversion.files]]
filename = "pyproject.toml"
search = 'version = "{current_version}"'
replace = 'version = "{new_version}"'

[[tool.bumpversion.files]]
filename = "screenshot_cleaner/__init__.py"
search = '__version__ = "{current_version}"'
replace = '__version__ = "{new_version}"'
```

**Integration with CI/CD:**
The version management integrates with GitHub Actions or other CI/CD pipelines:
- Automated releases on version tags
- Changelog generation
- PyPI package publishing

**Best Practices:**
1. Always commit changes before bumping version
2. Use conventional commits for clear changelog generation
3. Test thoroughly before bumping major versions
4. Document breaking changes in CHANGELOG.md


## CI/CD Pipeline

### Overview

The project uses GitHub Actions for continuous integration and continuous deployment. The pipeline is defined in `.github/workflows/main.yml` and provides automated testing, building, and publishing.

### Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Trigger Events                            │
│  • Push to main/develop                                      │
│  • Pull requests                                             │
│  • Version tags (v*)                                         │
│  • Manual workflow dispatch                                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Test Stage                                │
│  • Run on macOS (required for this project)                  │
│  • Test Python 3.12 and 3.13                                 │
│  • Unit tests with pytest                                    │
│  • Coverage verification (≥90%)                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Integration Test Stage                          │
│  • End-to-end CLI testing                                    │
│  • Real file operations                                      │
│  • Command verification                                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                Build Stage (Conditional)                     │
│  • Only on tags or manual trigger                            │
│  • Build wheel and source distribution                       │
│  • Upload artifacts                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│   Publish to PyPI        │  │  Publish to Test PyPI    │
│   (on tags only)         │  │  (manual only)           │
│   • Trusted publishing   │  │  • For testing           │
│   • No tokens needed     │  │                          │
└──────────┬───────────────┘  └──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│                GitHub Release Stage                          │
│  • Extract changelog                                         │
│  • Create release                                            │
│  • Attach distribution files                                 │
└─────────────────────────────────────────────────────────────┘
```

### Job Definitions

#### 1. Test Job

**Purpose:** Verify code quality and functionality

**Configuration:**
- **Platform:** macOS-latest (required for screenshot functionality)
- **Python versions:** 3.12, 3.13 (matrix strategy)
- **Runs on:** All pushes, PRs, and tags

**Steps:**
1. Checkout code
2. Install uv package manager
3. Set up Python environment
4. Install project dependencies
5. Run linting (placeholder for future)
6. Execute pytest test suite
7. Generate coverage report
8. Verify coverage ≥90%
9. Upload coverage to Codecov

**Exit Criteria:**
- All tests must pass
- Coverage must be ≥90%
- No critical linting errors

#### 2. Integration Test Job

**Purpose:** Validate end-to-end functionality

**Configuration:**
- **Platform:** macOS-latest
- **Depends on:** test job
- **Python version:** 3.12

**Steps:**
1. Run integration test suite
2. Test CLI commands with real files
3. Verify preview command
4. Verify clean command with dry-run
5. Test error handling

**Exit Criteria:**
- All integration tests pass
- CLI commands execute successfully

#### 3. Build Job

**Purpose:** Create distribution packages

**Configuration:**
- **Platform:** ubuntu-latest
- **Depends on:** test, integration-test
- **Runs only when:** Tag pushed OR manual trigger

**Steps:**
1. Build wheel distribution
2. Build source distribution
3. Upload artifacts for publishing

**Outputs:**
- `screenshots_cleaner-*.whl` (wheel)
- `screenshots-cleaner-*.tar.gz` (source)

#### 4. Publish to PyPI Job

**Purpose:** Publish release to Python Package Index

**Configuration:**
- **Platform:** ubuntu-latest
- **Depends on:** build
- **Runs only when:** Version tag pushed (v*)
- **Environment:** pypi
- **Permissions:** id-token: write (for trusted publishing)

**Steps:**
1. Download build artifacts
2. Publish to PyPI using trusted publishing

**Security:**
- Uses OIDC trusted publishing (no API tokens)
- Requires PyPI trusted publisher configuration
- Protected by GitHub environment

#### 5. Publish to Test PyPI Job

**Purpose:** Test releases before production

**Configuration:**
- **Platform:** ubuntu-latest
- **Depends on:** build
- **Runs only when:** Manual workflow dispatch with test flag
- **Environment:** test-pypi

**Steps:**
1. Download build artifacts
2. Publish to Test PyPI

**Use Case:**
- Testing package installation
- Verifying metadata
- Dry-run before production

#### 6. GitHub Release Job

**Purpose:** Create GitHub release with artifacts

**Configuration:**
- **Platform:** ubuntu-latest
- **Depends on:** publish-to-pypi
- **Runs only when:** Version tag pushed
- **Permissions:** contents: write

**Steps:**
1. Extract version from tag
2. Extract changelog section for version
3. Create GitHub release
4. Attach distribution files

### Workflow Triggers

#### Automatic Triggers

**Push to main/develop:**
```yaml
on:
  push:
    branches: [ main, develop ]
```
- Runs: test, integration-test
- Skips: build, publish

**Version tag:**
```yaml
on:
  push:
    tags:
      - 'v*'
```
- Runs: ALL jobs
- Publishes to PyPI
- Creates GitHub release

**Pull request:**
```yaml
on:
  pull_request:
    branches: [ main, develop ]
```
- Runs: test, integration-test
- Provides PR status checks

#### Manual Trigger

**Workflow dispatch:**
```yaml
on:
  workflow_dispatch:
    inputs:
      test_pypi:
        type: boolean
        default: false
```
- Can be triggered from GitHub UI
- Optional Test PyPI publishing
- Useful for testing releases

### Security Considerations

#### Trusted Publishing

The pipeline uses PyPI's Trusted Publishers feature:

**Benefits:**
- No API tokens to manage
- No secrets in repository
- OIDC-based authentication
- Automatic token rotation
- Audit trail

**Configuration Required:**
1. PyPI account with 2FA enabled
2. Trusted publisher configured on PyPI
3. GitHub environment named `pypi`
4. Workflow name: `main.yml`

#### Environment Protection

GitHub environments provide:
- Required reviewers (optional)
- Wait timers (optional)
- Deployment branch restrictions
- Audit logs

### Dependency Management

**uv Package Manager:**
- Fast dependency resolution
- Reproducible builds
- Lock file support
- Virtual environment management

**Caching:**
- uv cache enabled in workflow
- Speeds up subsequent runs
- Reduces network usage

### Monitoring and Observability

**Status Badges:**
- CI/CD status in README
- PyPI version badge
- Python version badge
- License badge

**Logs:**
- Detailed job logs in GitHub Actions
- Coverage reports in Codecov
- Build artifacts available for download

**Notifications:**
- GitHub commit status checks
- PR check status
- Email notifications on failure

### Failure Handling

**Test Failures:**
- Pipeline stops immediately
- No build or publish occurs
- PR cannot be merged (if required)

**Build Failures:**
- Publish jobs are skipped
- Artifacts not created
- Tag remains but no release

**Publish Failures:**
- GitHub release not created
- Manual intervention required
- Can retry by re-pushing tag

### Best Practices

1. **Always run tests locally** before pushing
2. **Use Test PyPI** for testing releases
3. **Review workflow logs** after each run
4. **Keep dependencies updated** (Dependabot)
5. **Monitor coverage trends**
6. **Update CHANGELOG** before releases
7. **Use semantic versioning** for tags

### Future Enhancements

Potential pipeline improvements:

1. **Code Quality:**
   - Add ruff linting
   - Add mypy type checking
   - Add bandit security scanning

2. **Testing:**
   - Add performance benchmarks
   - Add mutation testing
   - Add property-based testing

3. **Deployment:**
   - Add Docker image building
   - Add Homebrew formula updates
   - Add documentation deployment

4. **Notifications:**
   - Slack notifications
   - Discord webhooks
   - Email summaries

## PyPI Package Configuration

### Package Metadata

The package is configured in `pyproject.toml` with comprehensive metadata:

**Basic Information:**
- Name: `screenshots-cleaner`
- Description: CLI tool for cleaning up old macOS screenshots
- License: MIT
- Python requirement: ≥3.12

**Project URLs:**
- Homepage: GitHub repository
- Documentation: README
- Repository: GitHub
- Issues: GitHub Issues
- Changelog: CHANGELOG.md

**Classifiers:**
- Development Status: Beta
- Environment: Console
- Intended Audience: Developers, End Users
- Operating System: macOS
- Programming Language: Python 3.12+
- Topic: System/Filesystems, Utilities

**Keywords:**
- macos, screenshots, cleanup, cli, automation, desktop, file-management

### Build System

**Build backend:** hatchling
- Modern Python build backend
- Fast and reliable
- Supports all standard features

**Package structure:**
```
screenshots-cleaner/
├── pyproject.toml          # Package configuration
├── README.md               # Package description
├── CHANGELOG.md            # Version history
├── LICENSE                 # MIT license
└── screenshots_cleaner/    # Package code
    ├── __init__.py         # Version info
    ├── cli.py              # Entry point
    ├── core/               # Core modules
    └── utils/              # Utilities
```

### Installation Methods

**From PyPI:**
```bash
pip install screenshots-cleaner
uv tool install screenshots-cleaner
```

**From source:**
```bash
git clone <repo>
cd screenshot-cleaner
uv sync
uv run screenshots-cleaner
```

**Development install:**
```bash
uv sync
uv run pytest
```

### Version Management Integration

The package version is managed by bump-my-version:
- Single source of truth in `pyproject.toml`
- Automatically updated in `__init__.py`
- Git tags created automatically
- Triggers CI/CD pipeline on tag push
