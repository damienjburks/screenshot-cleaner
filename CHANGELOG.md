# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Automated version management with bump-my-version
- Comprehensive documentation for version bumping workflow

## [0.1.0] - 2024-11-16

### Added
- Initial release of Screenshot Cleaner
- macOS screenshot detection and cleanup
- `preview` command to see files that would be deleted
- `clean` command to delete old screenshots
- Dry-run mode for safe testing
- Force mode to skip confirmation prompts
- Custom age threshold (default: 7 days)
- Custom directory path support
- Rich console output with tables
- Optional file logging
- Comprehensive test suite (96% coverage)
- macOS LaunchAgent automation documentation
- Python Fire CLI framework
- uv package manager support

### Features
- Smart screenshot pattern matching
- Safe deletion with confirmation prompts
- Efficient directory scanning
- Error handling for permission issues
- No subdirectory traversal (safety feature)

[Unreleased]: https://github.com/damienjburks/screenshot-cleaner/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/damienjburks/screenshot-cleaner/releases/tag/v0.1.0
