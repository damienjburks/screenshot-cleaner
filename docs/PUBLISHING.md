# Publishing to PyPI

This document explains how to publish Screenshot Cleaner to PyPI using the automated GitHub Actions workflow.

## Overview

The project uses GitHub Actions with uv to automatically build and publish packages to PyPI when you create a new version tag. The workflow uses PyPI's Trusted Publishers feature for secure, token-free publishing.

## Prerequisites

### 1. PyPI Account Setup

1. Create an account on [PyPI](https://pypi.org/account/register/)
2. Enable 2FA (required for trusted publishing)

### 2. Configure Trusted Publishing on PyPI

**Important:** Set this up BEFORE creating your first release.

1. Go to [PyPI Publishing Settings](https://pypi.org/manage/account/publishing/)
2. Scroll to "Add a new pending publisher"
3. Fill in the form:
   - **PyPI Project Name**: `screenshots-cleaner`
   - **Owner**: Your GitHub username or organization
   - **Repository name**: `screenshot-cleaner`
   - **Workflow name**: `main.yml`
   - **Environment name**: `pypi`
4. Click "Add"

### 3. Test PyPI (Optional but Recommended)

For testing releases, also set up Test PyPI:

1. Create account on [Test PyPI](https://test.pypi.org/account/register/)
2. Configure trusted publisher:
   - **PyPI Project Name**: `screenshots-cleaner`
   - **Owner**: Your GitHub username
   - **Repository name**: `screenshot-cleaner`
   - **Workflow name**: `main.yml`
   - **Environment name**: `test-pypi`

### 4. GitHub Repository Settings

1. Go to your repository settings
2. Navigate to **Environments**
3. Create environment named `pypi`
4. (Optional) Add protection rules:
   - Required reviewers
   - Wait timer
   - Deployment branches (only `main`)

## Publishing Workflow

### Automatic Publishing (Recommended)

The easiest way to publish is using the automated release script:

```bash
# This will:
# 1. Run tests
# 2. Bump version
# 3. Create git tag
# 4. Push to GitHub
# 5. Trigger automatic PyPI publish
./scripts/release.sh patch
```

### Manual Publishing

1. **Ensure everything is ready:**
   ```bash
   # Run tests
   uv run pytest --cov=screenshot_cleaner
   
   # Update CHANGELOG.md
   vim CHANGELOG.md
   
   # Commit changes
   git add .
   git commit -m "Prepare release"
   ```

2. **Bump version:**
   ```bash
   uv run bump-my-version bump patch
   ```

3. **Push with tags:**
   ```bash
   git push
   git push --tags
   ```

4. **GitHub Actions automatically:**
   - Runs tests on macOS
   - Builds the package
   - Publishes to PyPI
   - Creates GitHub release

## What Happens During Publishing

### 1. Test Job
- Checks out code
- Installs uv and Python
- Runs full test suite
- Verifies 90% coverage threshold

### 2. Build Job
- Builds wheel and source distribution
- Uploads artifacts for publishing

### 3. Publish to PyPI Job
- Downloads built distributions
- Publishes to PyPI using trusted publishing
- No API tokens needed!

### 4. GitHub Release Job
- Creates GitHub release
- Extracts changelog for version
- Attaches distribution files

## Testing Before Publishing

### Test Locally

Build and inspect the package locally:

```bash
# Build package
uv build

# Check contents
tar -tzf dist/screenshot-cleaner-*.tar.gz
unzip -l dist/screenshot_cleaner-*.whl

# Install locally and test
uv pip install dist/screenshot_cleaner-*.whl
screenshot-cleaner --help
```

### Test on Test PyPI

Publish to Test PyPI first:

1. Go to GitHub Actions
2. Run "Publish to PyPI" workflow manually
3. Check "Publish to Test PyPI instead of PyPI"
4. Click "Run workflow"

Install from Test PyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ screenshot-cleaner
```

## Monitoring Releases

### GitHub Actions

Monitor the workflow:
1. Go to **Actions** tab in GitHub
2. Click on "Publish to PyPI" workflow
3. View logs for each job

### PyPI

Check your package:
- Production: https://pypi.org/project/screenshot-cleaner/
- Test: https://test.pypi.org/project/screenshot-cleaner/

## Troubleshooting

### "Trusted publishing exchange failure"

**Problem:** PyPI trusted publisher not configured correctly.

**Solution:**
1. Verify publisher settings on PyPI
2. Ensure workflow name matches exactly: `main.yml`
3. Ensure environment name matches: `pypi`
4. Check repository owner/name are correct

### "Package already exists"

**Problem:** Version already published to PyPI.

**Solution:**
- You cannot overwrite existing versions
- Bump to a new version number
- Delete the git tag and re-release:
  ```bash
  git tag -d v0.1.1
  git push origin :refs/tags/v0.1.1
  ```

### Tests failing in CI

**Problem:** Tests pass locally but fail in GitHub Actions.

**Solution:**
1. Check Python version compatibility
2. Review test logs in Actions tab
3. Test on macOS locally (required for this project)
4. Check for environment-specific issues

### Build artifacts missing

**Problem:** Distribution files not found.

**Solution:**
1. Ensure `uv build` completes successfully
2. Check build job logs
3. Verify `dist/` directory contains files

## Manual Publishing (Emergency)

If GitHub Actions fails, you can publish manually:

```bash
# Install build tools
uv add --dev build twine

# Build package
uv build

# Upload to PyPI (requires API token)
uv run twine upload dist/*

# Or to Test PyPI
uv run twine upload --repository testpypi dist/*
```

**Note:** Manual publishing requires API tokens. Trusted publishing is preferred.

## Security Best Practices

1. ✅ **Use Trusted Publishing** - No API tokens to manage
2. ✅ **Enable 2FA** on PyPI account
3. ✅ **Protect main branch** - Require PR reviews
4. ✅ **Use environments** - Add approval requirements
5. ✅ **Review releases** - Check before publishing
6. ❌ **Never commit tokens** - Use GitHub secrets if needed

## Version Strategy

Follow semantic versioning:

- **Patch** (0.1.0 → 0.1.1): Bug fixes
- **Minor** (0.1.0 → 0.2.0): New features
- **Major** (0.1.0 → 1.0.0): Breaking changes

## Post-Release Checklist

After publishing:

- [ ] Verify package on PyPI
- [ ] Test installation: `pip install screenshot-cleaner`
- [ ] Check GitHub release notes
- [ ] Update documentation if needed
- [ ] Announce release (if applicable)
- [ ] Close related issues
- [ ] Update project board

## Resources

- [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions for Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Semantic Versioning](https://semver.org/)
