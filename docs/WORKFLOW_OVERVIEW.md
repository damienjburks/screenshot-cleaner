# GitHub Actions Workflow Overview

This document explains the consolidated CI/CD workflow in `.github/workflows/main.yml`.

## Workflow Structure

The workflow is organized into dependent jobs that run sequentially:

```
┌─────────────┐
│    Test     │ (Python 3.12 & 3.13)
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Integration Test│
└────────┬────────┘
         │
         ▼
    ┌────────┐
    │ Build  │ (only on tags/manual)
    └───┬────┘
        │
        ├──────────────┬──────────────┐
        ▼              ▼              ▼
  ┌─────────┐   ┌──────────┐   ┌──────────┐
  │ Publish │   │ Test PyPI│   │ GitHub   │
  │  PyPI   │   │ (manual) │   │ Release  │
  └─────────┘   └──────────┘   └──────────┘
```

## Jobs

### 1. Test (Required)
**Runs on:** Every push, PR, and tag
**Platform:** macOS
**Python:** 3.12 and 3.13

**Steps:**
- Checkout code
- Install uv and Python
- Install dependencies
- Run linting (placeholder)
- Run unit tests
- Check coverage (must be ≥90%)
- Upload coverage to Codecov

**Purpose:** Ensures code quality and test coverage before any deployment.

### 2. Integration Test (Required)
**Runs on:** After test job passes
**Platform:** macOS
**Depends on:** `test`

**Steps:**
- Run integration tests
- Test CLI commands
- Verify end-to-end functionality

**Purpose:** Validates the complete application workflow.

### 3. Build (Conditional)
**Runs on:** Tags (v*) or manual workflow dispatch
**Platform:** Ubuntu
**Depends on:** `test`, `integration-test`

**Steps:**
- Build wheel and source distribution
- Upload artifacts for publishing

**Purpose:** Creates distributable packages only when needed.

### 4. Publish to PyPI (Conditional)
**Runs on:** Tags only (v*)
**Platform:** Ubuntu
**Depends on:** `build`
**Environment:** `pypi`

**Steps:**
- Download build artifacts
- Publish to PyPI using trusted publishing

**Purpose:** Automatically publishes releases to PyPI.

### 5. Publish to Test PyPI (Conditional)
**Runs on:** Manual workflow dispatch with test flag
**Platform:** Ubuntu
**Depends on:** `build`
**Environment:** `test-pypi`

**Steps:**
- Download build artifacts
- Publish to Test PyPI

**Purpose:** Allows testing releases before production.

### 6. GitHub Release (Conditional)
**Runs on:** Tags only (v*)
**Platform:** Ubuntu
**Depends on:** `publish-to-pypi`

**Steps:**
- Extract version from tag
- Extract changelog for version
- Create GitHub release with artifacts

**Purpose:** Creates GitHub release with distribution files.

## Triggers

### Automatic Triggers

**Push to main/develop:**
```yaml
on:
  push:
    branches: [ main, develop ]
```
- Runs: test, integration-test
- Skips: build, publish

**Push tag (v*):**
```yaml
on:
  push:
    tags:
      - 'v*'
```
- Runs: ALL jobs
- Publishes to PyPI
- Creates GitHub release

**Pull Request:**
```yaml
on:
  pull_request:
    branches: [ main, develop ]
```
- Runs: test, integration-test
- Skips: build, publish

### Manual Trigger

**Workflow Dispatch:**
```yaml
on:
  workflow_dispatch:
    inputs:
      test_pypi:
        type: boolean
        default: false
```
- Can run from GitHub Actions tab
- Option to publish to Test PyPI
- Useful for testing releases

## Dependency Chain

The workflow enforces this dependency chain:

1. **test** must pass
2. **integration-test** must pass (depends on test)
3. **build** runs only if tests pass AND (tag exists OR manual trigger)
4. **publish-to-pypi** runs only if build succeeds AND tag exists
5. **publish-to-test-pypi** runs only if build succeeds AND manual trigger with test flag
6. **github-release** runs only if publish-to-pypi succeeds

## Environment Variables

No environment variables are required. The workflow uses:
- GitHub context variables (`github.ref`, `github.event_name`)
- Trusted publishing (no API tokens needed)

## Secrets

No secrets are required! The workflow uses:
- **Trusted Publishing** for PyPI (OIDC authentication)
- **GitHub token** (automatically provided)

## Usage Examples

### Regular Development

```bash
# Make changes
git add .
git commit -m "feat: Add new feature"
git push origin main
```
**Result:** Tests run, no publish

### Create Release

```bash
# Use release script
./scripts/release.sh patch

# Or manually
uv run bump-my-version bump patch
git push && git push --tags
```
**Result:** Tests run, build, publish to PyPI, create GitHub release

### Test Release

1. Go to GitHub Actions
2. Click "CI/CD" workflow
3. Click "Run workflow"
4. Check "Publish to Test PyPI"
5. Click "Run workflow"

**Result:** Tests run, build, publish to Test PyPI only

## Monitoring

### View Workflow Runs

1. Go to repository on GitHub
2. Click "Actions" tab
3. Click on a workflow run
4. View logs for each job

### Check Status

- **Badge in README**: Shows latest status
- **Commit status**: Shows check status on commits
- **PR checks**: Shows required checks on PRs

## Troubleshooting

### Tests fail but pass locally

- Check Python version (3.12 or 3.13)
- Ensure running on macOS
- Review GitHub Actions logs
- Check for environment-specific issues

### Build doesn't run

- Verify you pushed a tag (v*)
- Or triggered workflow manually
- Check job conditions in workflow file

### Publish fails

- Verify trusted publisher configured on PyPI
- Check environment name matches: `pypi`
- Ensure workflow name is: `main.yml`
- Verify 2FA enabled on PyPI account

### GitHub release not created

- Ensure publish-to-pypi succeeded
- Check CHANGELOG.md has entry for version
- Review github-release job logs

## Best Practices

1. ✅ **Always run tests locally** before pushing
2. ✅ **Use Test PyPI** before production releases
3. ✅ **Review workflow logs** after each run
4. ✅ **Keep dependencies updated** (Dependabot)
5. ✅ **Monitor coverage** (should stay ≥90%)
6. ✅ **Update CHANGELOG** before releases

## Customization

### Add Linting

Replace the placeholder in test job:

```yaml
- name: Run linting
  run: |
    uv add --dev ruff
    uv run ruff check .
```

### Add More Tests

Add additional test jobs:

```yaml
security-scan:
  name: Security Scan
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Run Bandit
      run: |
        uv add --dev bandit
        uv run bandit -r screenshots_cleaner/
```

### Change Python Versions

Update the matrix:

```yaml
strategy:
  matrix:
    python-version: ['3.12', '3.13', '3.14']
```

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- [uv Documentation](https://docs.astral.sh/uv/)
