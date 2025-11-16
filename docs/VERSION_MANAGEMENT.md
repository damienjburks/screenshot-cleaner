# Version Management Guide

This document explains how version management works in Screenshot Cleaner.

## Overview

Screenshot Cleaner uses [bump-my-version](https://github.com/callowayproject/bump-my-version) for automated semantic versioning. This ensures consistent version numbers across all project files and simplifies the release process.

## Semantic Versioning

We follow [Semantic Versioning 2.0.0](https://semver.org/):

```
MAJOR.MINOR.PATCH
```

- **MAJOR** (1.0.0): Incompatible API changes (breaking changes)
- **MINOR** (0.1.0): New functionality (backward compatible)
- **PATCH** (0.0.1): Bug fixes (backward compatible)

### Examples

- `0.1.0` → `0.1.1`: Bug fix (patch)
- `0.1.0` → `0.2.0`: New feature (minor)
- `0.1.0` → `1.0.0`: Breaking change (major)

## Configuration

Version management is configured in `.bumpversion.toml`:

```toml
[tool.bumpversion]
current_version = "0.1.0"
commit = true
tag = true
tag_name = "v{new_version}"
```

### Files Updated

When bumping version, these files are automatically updated:

1. `pyproject.toml` - Project version
2. `screenshot_cleaner/__init__.py` - Package version
3. `.bumpversion.toml` - Current version tracking

## Usage

### Quick Start

Use the automated release script:

```bash
./scripts/release.sh patch   # Bug fixes
./scripts/release.sh minor   # New features
./scripts/release.sh major   # Breaking changes
```

### Manual Commands

```bash
# Show current version
uv run bump-my-version show current_version

# Preview changes (dry-run)
uv run bump-my-version bump patch --dry-run --verbose

# Bump patch version (0.1.0 → 0.1.1)
uv run bump-my-version bump patch

# Bump minor version (0.1.0 → 0.2.0)
uv run bump-my-version bump minor

# Bump major version (0.1.0 → 1.0.0)
uv run bump-my-version bump major
```

## Workflow

### Standard Release Process

1. **Make changes** and commit them:
   ```bash
   git add .
   git commit -m "feat: Add new feature"
   ```

2. **Run tests**:
   ```bash
   uv run pytest --cov=screenshot_cleaner
   ```

3. **Update CHANGELOG.md**:
   ```markdown
   ## [Unreleased]
   
   ### Added
   - New feature description
   ```

4. **Bump version**:
   ```bash
   ./scripts/release.sh minor
   ```
   
   Or manually:
   ```bash
   uv run bump-my-version bump minor
   ```

5. **Push changes**:
   ```bash
   git push
   git push --tags
   ```

6. **Create GitHub release**:
   - Go to GitHub → Releases → New Release
   - Select the new tag (e.g., `v0.2.0`)
   - Copy CHANGELOG entry to release notes
   - Publish release

### What Happens During Bump

When you run `bump-my-version bump [part]`:

1. ✅ Version updated in `pyproject.toml`
2. ✅ Version updated in `screenshot_cleaner/__init__.py`
3. ✅ Version updated in `.bumpversion.toml`
4. ✅ Git commit created: `"Bump version: 0.1.0 → 0.2.0"`
5. ✅ Git tag created: `v0.2.0`

## Safety Features

### Dirty Working Directory Check

bump-my-version prevents version bumps when you have uncommitted changes:

```bash
$ uv run bump-my-version bump patch
Error: Git working directory is not clean
```

**Override** (not recommended):
```bash
uv run bump-my-version bump patch --allow-dirty
```

### Dry Run

Always preview changes before committing:

```bash
uv run bump-my-version bump patch --dry-run --verbose
```

This shows:
- Which files will be modified
- Exact changes to be made
- Git commit message
- Git tag that will be created

## Best Practices

### Before Bumping

- ✅ Commit all changes
- ✅ Run full test suite
- ✅ Update CHANGELOG.md
- ✅ Review changes with dry-run
- ✅ Ensure CI/CD passes

### Choosing Version Type

**Patch (0.1.0 → 0.1.1):**
- Bug fixes
- Documentation updates
- Performance improvements
- No new features
- No breaking changes

**Minor (0.1.0 → 0.2.0):**
- New features
- New functionality
- Backward compatible
- Deprecations (with warnings)

**Major (0.1.0 → 1.0.0):**
- Breaking changes
- Removed features
- Changed APIs
- Incompatible updates

### After Bumping

1. Verify the tag was created:
   ```bash
   git tag -l
   ```

2. Push immediately:
   ```bash
   git push && git push --tags
   ```

3. Create GitHub release with notes

4. Announce the release (if applicable)

## Troubleshooting

### "Git working directory is not clean"

**Problem:** You have uncommitted changes.

**Solution:**
```bash
git status
git add .
git commit -m "Your changes"
```

### "Version already exists"

**Problem:** Tag already exists in git.

**Solution:**
```bash
# Delete local tag
git tag -d v0.1.1

# Delete remote tag
git push origin :refs/tags/v0.1.1
```

### Wrong version bumped

**Problem:** Bumped wrong version type.

**Solution:**
```bash
# Reset the commit (keeps changes)
git reset HEAD~1

# Or hard reset (discards changes)
git reset --hard HEAD~1

# Delete the tag
git tag -d v0.1.1
```

## Advanced Usage

### Custom Version Format

Edit `.bumpversion.toml` to customize version format:

```toml
[tool.bumpversion]
parse = "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)"
serialize = ["{major}.{minor}.{patch}"]
```

### Pre-release Versions

Add pre-release support:

```toml
serialize = [
    "{major}.{minor}.{patch}-{release}",
    "{major}.{minor}.{patch}"
]

[tool.bumpversion.parts.release]
values = ["dev", "rc", "final"]
```

Usage:
```bash
uv run bump-my-version bump release  # 0.1.0 → 0.1.0-dev
```

### Skip Git Operations

Bump version without git commit/tag:

```bash
uv run bump-my-version bump patch --no-commit --no-tag
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
```

## References

- [bump-my-version Documentation](https://callowayproject.github.io/bump-my-version/)
- [Semantic Versioning Specification](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
