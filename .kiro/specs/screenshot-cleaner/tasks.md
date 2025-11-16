# Implementation Plan

- [x] 1. Set up project structure and core interfaces
  - Initialize project using `uv init screenshots-cleaner`
  - Set Python version with `uv python pin 3.12`
  - Create directory structure: `core/`, `utils/`, `tests/`
  - Add dependencies: `uv add fire rich`
  - Add dev dependencies: `uv add --dev pytest pytest-cov pytest-mock`
  - Create `__init__.py` files in all package directories
  - Configure `pyproject.toml` with project metadata and script entry point
  - Create `.gitignore` file
  - _Requirements: 7.1, 7.2, 7.3_

- [x] 2. Implement platform detection module
  - [x] 2.1 Create `core/platform.py` with OS detection functions
    - Implement `is_macos()` function using `platform.system()`
    - Implement `validate_macos()` function that raises SystemExit on non-macOS
    - Add clear error messages for non-macOS platforms
    - _Requirements: 6.1, 6.2, 6.3_
  
  - [x] 2.2 Write unit tests for platform module
    - Create `tests/core/test_platform.py`
    - Mock `platform.system()` to test Darwin and non-Darwin cases
    - Test `is_macos()` returns correct boolean values
    - Test `validate_macos()` raises SystemExit with proper exit code
    - _Requirements: 6.1, 6.2, 6.3_

- [x] 3. Implement scanner module for file discovery
  - [x] 3.1 Create `core/scanner.py` with screenshot discovery logic
    - Implement `get_default_screenshot_dir()` to return `~/Desktop`
    - Implement `matches_screenshot_pattern()` with regex for "Screen Shot *.png" and "Screenshot *.png"
    - Implement `get_file_age_days()` using file modification time
    - Implement `find_expired_files()` that combines pattern matching and age filtering
    - Use `os.scandir()` for efficient directory listing
    - Ensure no subdirectory traversal
    - _Requirements: 1.1, 2.1, 2.2, 2.3, 2.4, 8.1, 8.2, 8.3, 9.1, 9.2_
  
  - [x] 3.2 Write unit tests for scanner module
    - Create `tests/core/test_scanner.py`
    - Test pattern matching with valid and invalid filenames
    - Test age calculation with mocked timestamps
    - Test `find_expired_files()` with temporary test files
    - Verify no subdirectory traversal occurs
    - Test empty directory and permission error handling
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 8.1, 8.2, 8.3_

- [x] 4. Implement cleanup module for file deletion
  - [x] 4.1 Create `core/cleanup.py` with deletion logic
    - Implement `delete_file()` with dry-run support
    - Implement `delete_files()` for batch deletion
    - Add error handling for individual file failures
    - Ensure files are only deleted within target directory
    - Return success/failure counts
    - _Requirements: 3.1, 3.2, 8.4_
  
  - [x] 4.2 Write unit tests for cleanup module
    - Create `tests/core/test_cleanup.py`
    - Test dry-run mode doesn't delete files
    - Test actual deletion with temporary files
    - Test error handling for permission errors
    - Verify success/failure counting
    - Test batch deletion with mixed results
    - Verify path safety (no deletion outside target)
    - _Requirements: 3.1, 3.2, 8.4_

- [x] 5. Implement logging utilities
  - [x] 5.1 Create `utils/logging.py` with logging configuration
    - Implement `setup_logger()` with stdout and optional file output
    - Implement `log_info()`, `log_error()` helper functions
    - Implement `log_file_operation()` for file operation logging
    - Use Rich console for colorized output
    - Format logs with timestamps
    - _Requirements: 4.1, 4.2, 4.3, 4.4_
  
  - [x] 5.2 Write unit tests for logging module
    - Create `tests/utils/test_logging.py`
    - Test stdout output format and content
    - Test file output when log_file is specified
    - Test log levels and formatting
    - Test timestamp formatting
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [x] 6. Implement CLI interface with Python Fire
  - [x] 6.1 Create `cli.py` with ScreenshotCleaner class
    - Create `ScreenshotCleaner` class with `preview()` and `clean()` methods
    - Implement `preview()` command that runs in dry-run mode
    - Implement `clean()` command with force and dry-run flags
    - Add confirmation prompt for clean command (unless force=True)
    - Call `validate_macos()` at start of each command
    - Use Rich tables to display file lists
    - Handle all command-line arguments (path, days, force, dry_run, log_file)
    - Implement `main()` function that calls `fire.Fire(ScreenshotCleaner)`
    - Add proper exit codes for different error conditions
    - _Requirements: 1.2, 2.2, 3.1, 3.2, 3.3, 4.1, 4.2, 5.1, 5.2, 6.1, 6.2, 6.3_
  
  - [x] 6.2 Write unit tests for CLI module
    - Create `tests/test_cli.py`
    - Test `preview` command with various arguments
    - Test `clean` command with force flag
    - Test `clean` command with dry-run flag
    - Mock user input for confirmation prompt tests
    - Test error handling and exit codes
    - Test integration with Fire framework
    - _Requirements: 3.1, 3.2, 3.3, 5.1, 5.2_

- [x] 7. Configure packaging and entry point
  - [x] 7.1 Update `pyproject.toml` with script entry point
    - Add `[project.scripts]` section with `screenshots-cleaner = "screenshots_cleaner.cli:main"`
    - Ensure all dependencies are properly declared
    - Add project metadata (name, version, description, authors)
    - _Requirements: 7.1, 7.2, 7.3_
  
  - [x] 7.2 Test local execution with uv
    - Run `uv run screenshots-cleaner preview` to test local execution
    - Run `uv run screenshots-cleaner clean --dry-run` to verify dry-run mode
    - Verify all command-line arguments work correctly
    - _Requirements: 7.1_
  
  - [x] 7.3 Test global installation with uv
    - Run `uv tool install .` to install globally
    - Verify `screenshots-cleaner` command works from any directory
    - Test `uv tool uninstall screenshots-cleaner` for cleanup
    - _Requirements: 7.2_

- [x] 8. Create documentation
  - [x] 8.1 Write comprehensive README.md
    - Add project overview and features
    - Add installation instructions (uv run and uv tool install)
    - Add usage examples for preview and clean commands
    - Document all command-line arguments
    - Add macOS LaunchAgent setup instructions
    - Include example plist configurations (startup, daily, interval)
    - Add troubleshooting section
    - Add contributing guidelines for open-source
    - _Requirements: All_
  
  - [x] 8.2 Add inline code documentation
    - Add docstrings to all public functions and classes
    - Add type hints throughout the codebase
    - Add comments for complex logic
    - _Requirements: All_

- [x] 9. Set up test infrastructure and validate coverage
  - Create `tests/conftest.py` with shared fixtures
  - Configure pytest in `pyproject.toml`
  - Run full test suite with `uv run pytest`
  - Generate coverage report with `uv run pytest --cov=screenshots_cleaner --cov-report=html`
  - Verify minimum 90% code coverage
  - Fix any failing tests
  - _Requirements: All_

- [x] 10. Create integration test scenarios
  - Create test script that generates dummy screenshot files
  - Test preview command with various file ages
  - Test clean command with confirmation
  - Test clean command with --force flag
  - Test custom --path and --days arguments
  - Test --log-file output
  - Verify performance with large directories
  - _Requirements: 9.1, 9.2_
