# PyPI Setup Guide

Quick guide to set up PyPI publishing for Screenshot Cleaner.

## Step 1: Create PyPI Account

1. Go to https://pypi.org/account/register/
2. Create your account
3. Verify your email
4. **Enable 2FA** (required for trusted publishing)

## Step 2: Configure Trusted Publisher

**Do this BEFORE your first release!**

1. Go to https://pypi.org/manage/account/publishing/
2. Scroll to "Add a new pending publisher"
3. Fill in:
   ```
   PyPI Project Name: screenshots-cleaner
   Owner: YOUR_GITHUB_USERNAME
   Repository name: screenshot-cleaner
   Workflow name: main.yml
   Environment name: pypi
   ```
4. Click "Add"

## Step 3: GitHub Environment Setup

1. Go to your GitHub repository
2. Settings → Environments
3. Click "New environment"
4. Name it: `pypi`
5. (Optional) Add protection rules:
   - ✅ Required reviewers
   - ✅ Wait timer: 5 minutes
   - ✅ Deployment branches: `main` only

## Step 4: Test PyPI (Optional)

For testing releases:

1. Create account at https://test.pypi.org/account/register/
2. Configure trusted publisher:
   ```
   PyPI Project Name: screenshots-cleaner
   Owner: YOUR_GITHUB_USERNAME
   Repository name: screenshot-cleaner
   Workflow name: main.yml
   Environment name: test-pypi
   ```
3. Create GitHub environment: `test-pypi`

## Step 5: Update Repository URLs

Edit `pyproject.toml`:

```toml
[project.urls]
Homepage = "https://github.com/YOUR_USERNAME/screenshot-cleaner"
Repository = "https://github.com/YOUR_USERNAME/screenshot-cleaner"
Issues = "https://github.com/YOUR_USERNAME/screenshot-cleaner/issues"
```

## Step 6: First Release

```bash
# Make sure everything is committed
git status

# Run the release script
./scripts/release.sh patch

# This will:
# 1. Run tests
# 2. Create version 0.1.0
# 3. Push tag to GitHub
# 4. Trigger PyPI publish
```

## Step 7: Verify

1. Check GitHub Actions: https://github.com/YOUR_USERNAME/screenshot-cleaner/actions
2. Check PyPI: https://pypi.org/project/screenshot-cleaner/
3. Test installation:
   ```bash
   pip install screenshot-cleaner
   screenshot-cleaner --help
   ```

## Troubleshooting

### "Trusted publishing exchange failure"

- Double-check all settings match exactly
- Workflow name: `main.yml`
- Environment name: `pypi`
- Repository owner and name are correct

### "Package name already taken"

- Choose a different name in `pyproject.toml`
- Update trusted publisher settings with new name

### Tests failing in CI

- Ensure tests pass locally on macOS
- Check Python version compatibility
- Review GitHub Actions logs

## Security Notes

✅ **DO:**
- Use trusted publishing (no tokens!)
- Enable 2FA on PyPI
- Protect your main branch
- Review releases before publishing

❌ **DON'T:**
- Commit API tokens
- Skip tests before releasing
- Publish without reviewing changes
- Use same credentials across services

## Next Steps

After setup:
1. Read [PUBLISHING.md](PUBLISHING.md) for detailed workflow
2. Read [CONTRIBUTING.md](../CONTRIBUTING.md) for development guide
3. Make your first release!

## Resources

- [PyPI Trusted Publishers Guide](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Semantic Versioning](https://semver.org/)
