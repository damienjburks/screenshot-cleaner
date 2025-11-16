# Requirements Document

## Introduction

A Python CLI tool for macOS that automatically deletes screenshots older than a specified number of days. The tool must be installable and runnable using uv, support dry-run mode, and provide safe deletion controls to help users keep their screenshot folders clean without manual triage.

## Glossary

- **Screenshot Cleaner**: The Python CLI application that manages screenshot deletion
- **Target Directory**: The filesystem directory containing screenshots to be evaluated for deletion
- **Screenshot File**: An image file matching common macOS screenshot naming patterns (e.g., "Screen Shot *.png", "Screenshot *.png")
- **Expired File**: A screenshot file whose modification time exceeds the configured age threshold
- **Dry-Run Mode**: An execution mode where the Screenshot Cleaner identifies files for deletion but does not perform actual deletion
- **UV**: A Python package manager and tool runner used for environment management and CLI execution

## Requirements

### Requirement 1

**User Story:** As a macOS user with a cluttered screenshot folder, I want the tool to automatically find my system screenshot directory, so that I don't have to manually specify the location each time.

#### Acceptance Criteria

1. WHEN the Screenshot Cleaner executes without a path argument, THE Screenshot Cleaner SHALL identify the system default screenshot directory
2. WHERE the user provides a custom path argument, THE Screenshot Cleaner SHALL use the specified directory as the Target Directory
3. IF the Target Directory does not exist, THEN THE Screenshot Cleaner SHALL display an error message and terminate with a non-zero exit code

### Requirement 2

**User Story:** As a user who wants to clean up old files, I want to specify how old screenshots should be before deletion, so that I can control the retention period based on my needs.

#### Acceptance Criteria

1. THE Screenshot Cleaner SHALL accept a configurable age threshold in days for determining Expired Files
2. WHEN no age threshold is specified, THE Screenshot Cleaner SHALL use seven days as the default threshold
3. WHEN evaluating file age, THE Screenshot Cleaner SHALL compare the file modification time against the current system time
4. THE Screenshot Cleaner SHALL identify as Expired Files only those Screenshot Files whose age exceeds the configured threshold

### Requirement 3

**User Story:** As a cautious user, I want to preview which files will be deleted before actually deleting them, so that I can verify the tool won't remove files I want to keep.

#### Acceptance Criteria

1. WHEN the Screenshot Cleaner executes in Dry-Run Mode, THE Screenshot Cleaner SHALL display a list of Expired Files without performing deletion
2. WHEN the Screenshot Cleaner executes in Dry-Run Mode, THE Screenshot Cleaner SHALL display the count of files that would be deleted
3. THE Screenshot Cleaner SHALL provide a preview subcommand that executes in Dry-Run Mode

### Requirement 4

**User Story:** As a user who wants safe deletion, I want the tool to ask for confirmation before deleting files, so that I can prevent accidental data loss.

#### Acceptance Criteria

1. WHEN the Screenshot Cleaner executes a clean operation without force mode, THE Screenshot Cleaner SHALL prompt the user for confirmation before deleting files
2. WHERE the user provides a force flag, THE Screenshot Cleaner SHALL skip confirmation prompts and proceed with deletion
3. IF the user declines the confirmation prompt, THEN THE Screenshot Cleaner SHALL terminate without deleting files

### Requirement 5

**User Story:** As a user who needs to track what was deleted, I want the tool to log all actions, so that I have a record of deleted files.

#### Acceptance Criteria

1. THE Screenshot Cleaner SHALL output log messages to stdout for each file operation
2. THE Screenshot Cleaner SHALL include timestamps in log messages
3. WHERE the user specifies a log file path, THE Screenshot Cleaner SHALL write log messages to the specified file
4. WHEN a file is deleted, THE Screenshot Cleaner SHALL log the file path and deletion status

### Requirement 6

**User Story:** As a macOS user, I want the tool to only run on macOS systems, so that it doesn't attempt operations on unsupported platforms.

#### Acceptance Criteria

1. WHEN the Screenshot Cleaner starts, THE Screenshot Cleaner SHALL detect the operating system platform
2. IF the operating system is not macOS, THEN THE Screenshot Cleaner SHALL display an error message and terminate with a non-zero exit code
3. THE Screenshot Cleaner SHALL execute file operations only when running on macOS

### Requirement 7

**User Story:** As a developer using uv, I want to run the tool using uv commands, so that I can manage it consistently with my other Python tools.

#### Acceptance Criteria

1. THE Screenshot Cleaner SHALL be executable via the uv run command
2. THE Screenshot Cleaner SHALL be installable as a global tool via uv tool install
3. THE Screenshot Cleaner SHALL declare all dependencies in pyproject.toml for uv resolution

### Requirement 8

**User Story:** As a user concerned about safety, I want the tool to only delete files matching screenshot patterns, so that other files in the directory are never affected.

#### Acceptance Criteria

1. THE Screenshot Cleaner SHALL match files only against predefined screenshot naming patterns
2. THE Screenshot Cleaner SHALL evaluate for deletion only files within the Target Directory
3. THE Screenshot Cleaner SHALL NOT traverse subdirectories when identifying Screenshot Files
4. THE Screenshot Cleaner SHALL NOT delete files outside the Target Directory

### Requirement 9

**User Story:** As a user with large directories, I want the tool to complete quickly, so that I can use it regularly without waiting.

#### Acceptance Criteria

1. WHEN the Target Directory contains fewer than ten thousand files, THE Screenshot Cleaner SHALL complete execution within two seconds
2. THE Screenshot Cleaner SHALL process files efficiently without unnecessary filesystem operations


### Requirement 10

**User Story:** As a developer maintaining the project, I want automated version management, so that I can easily release new versions with consistent version numbering across all project files.

#### Acceptance Criteria

1. THE Screenshot Cleaner SHALL use semantic versioning (MAJOR.MINOR.PATCH) for version numbers
2. THE Screenshot Cleaner SHALL provide automated version bumping via bump-my-version tool
3. WHEN a version is bumped, THE Screenshot Cleaner SHALL update version numbers in pyproject.toml and __init__.py
4. THE Screenshot Cleaner SHALL support bumping major, minor, and patch version components
5. THE Screenshot Cleaner SHALL create git tags for version releases when configured


### Requirement 11

**User Story:** As a developer maintaining the project, I want automated CI/CD pipelines, so that code quality is verified and releases are published automatically when I create version tags.

#### Acceptance Criteria

1. THE Screenshot Cleaner SHALL run automated tests on every push and pull request
2. THE Screenshot Cleaner SHALL run tests on multiple Python versions (3.12 and 3.13)
3. THE Screenshot Cleaner SHALL verify test coverage meets minimum threshold (90%) before allowing deployment
4. WHEN a version tag is pushed, THE Screenshot Cleaner SHALL automatically build and publish to PyPI
5. THE Screenshot Cleaner SHALL use PyPI Trusted Publishers for secure, token-free publishing
6. THE Screenshot Cleaner SHALL create GitHub releases automatically when publishing to PyPI
7. THE Screenshot Cleaner SHALL run integration tests to verify end-to-end functionality
8. THE Screenshot Cleaner SHALL support manual workflow dispatch for testing releases on Test PyPI

### Requirement 12

**User Story:** As a project maintainer, I want the project published to PyPI, so that users can easily install it using pip or uv.

#### Acceptance Criteria

1. THE Screenshot Cleaner SHALL be published to the Python Package Index (PyPI)
2. THE Screenshot Cleaner SHALL be installable via pip install screenshots-cleaner
3. THE Screenshot Cleaner SHALL be installable via uv tool install screenshots-cleaner
4. THE Screenshot Cleaner SHALL include proper package metadata (description, keywords, classifiers)
5. THE Screenshot Cleaner SHALL include project URLs (homepage, repository, issues, changelog)
6. THE Screenshot Cleaner SHALL follow Python packaging best practices
