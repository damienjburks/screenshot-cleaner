# Implementation Plan

- [x] 1. Set up project structure and core interfaces
  - Initialize project using `uv init screenshot-cleaner`
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
    - Add `[project.scripts]` section with `screenshot-cleaner = "screenshot_cleaner.cli:main"`
    - Ensure all dependencies are properly declared
    - Add project metadata (name, version, description, authors)
    - _Requirements: 7.1, 7.2, 7.3_
  
  - [x] 7.2 Test local execution with uv
    - Run `uv run screenshot-cleaner preview` to test local execution
    - Run `uv run screenshot-cleaner clean --dry-run` to verify dry-run mode
    - Verify all command-line arguments work correctly
    - _Requirements: 7.1_
  
  - [x] 7.3 Test global installation with uv
    - Run `uv tool install .` to install globally
    - Verify `screenshot-cleaner` command works from any directory
    - Test `uv tool uninstall screenshot-cleaner` for cleanup
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
  - Generate coverage report with `uv run pytest --cov=screenshot_cleaner --cov-report=html`
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


- [x] 11. Set up automated version management
  - [x] 11.1 Install and configure bump-my-version
    - Add bump-my-version as dev dependency: `uv add --dev bump-my-version`
    - Create `.bumpversion.toml` configuration file
    - Configure version file locations (pyproject.toml, __init__.py)
    - Set up git commit and tag automation
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
  
  - [x] 11.2 Update documentation for version management
    - Add version bumping instructions to README.md
    - Document semantic versioning strategy
    - Add examples for patch, minor, and major releases
    - Document integration with release workflow
    - Create CHANGELOG.md
    - Create CONTRIBUTING.md
    - Create docs/VERSION_MANAGEMENT.md
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
  
  - [x] 11.3 Test version bumping workflow
    - Test patch version bump with dry-run
    - Test minor version bump with dry-run
    - Verify version updates in all configured files
    - Verify git commit and tag creation
    - Create release script (scripts/release.sh)
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [x] 12. Configure PyPI publishing
  - [x] 12.1 Update pyproject.toml for PyPI
    - Add comprehensive package metadata
    - Add project URLs (homepage, repository, issues, changelog)
    - Add keywords and classifiers
    - Configure build system with hatchling
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6_
  
  - [x] 12.2 Create PyPI publishing documentation
    - Create docs/PUBLISHING.md with complete publishing guide
    - Create docs/PYPI_SETUP.md with setup instructions
    - Create docs/RELEASE_CHECKLIST.md
    - Document trusted publisher configuration
    - Document Test PyPI workflow
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6_

- [x] 13. Set up CI/CD pipeline
  - [x] 13.1 Create GitHub Actions workflow
    - Create .github/workflows/main.yml
    - Configure test job for Python 3.12 and 3.13
    - Configure integration test job
    - Configure build job (conditional on tags)
    - Configure PyPI publish job with trusted publishing
    - Configure Test PyPI publish job (manual)
    - Configure GitHub release job
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7, 11.8_
  
  - [x] 13.2 Configure job dependencies
    - Make integration-test depend on test
    - Make build depend on test and integration-test
    - Make publish-to-pypi depend on build
    - Make github-release depend on publish-to-pypi
    - _Requirements: 11.1, 11.2, 11.3_
  
  - [x] 13.3 Set up workflow triggers
    - Configure push triggers for main/develop
    - Configure pull request triggers
    - Configure tag triggers (v*)
    - Configure manual workflow dispatch
    - _Requirements: 11.1, 11.4, 11.8_
  
  - [x] 13.4 Document CI/CD pipeline
    - Create docs/WORKFLOW_OVERVIEW.md
    - Update README with CI/CD badge
    - Document workflow structure and dependencies
    - Document security and best practices
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7, 11.8_
