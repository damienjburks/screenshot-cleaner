# Release Checklist

Use this checklist when preparing a new release.

## Pre-Release

- [ ] All changes committed and pushed
- [ ] Tests passing locally: `uv run pytest`
- [ ] Coverage above 90%: `uv run pytest --cov=screenshot_cleaner`
- [ ] CHANGELOG.md updated with changes
- [ ] Version number decided (patch/minor/major)
- [ ] Documentation updated if needed
- [ ] No open critical bugs

## Release

### Automated (Recommended)

- [ ] Run release script:
  ```bash
  ./scripts/release.sh [patch|minor|major]
  ```
- [ ] Verify tests pass in script
- [ ] Confirm version bump
- [ ] Script pushes tags automatically

### Manual

- [ ] Bump version:
  ```bash
  uv run bump-my-version bump [patch|minor|major]
  ```
- [ ] Push changes:
  ```bash
  git push && git push --tags
  ```

## Post-Release

- [ ] GitHub Actions workflow completes successfully
- [ ] Package appears on PyPI: https://pypi.org/project/screenshot-cleaner/
- [ ] GitHub release created with notes
- [ ] Test installation:
  ```bash
  pip install screenshot-cleaner
  screenshot-cleaner --help
  ```
- [ ] Verify version:
  ```bash
  pip show screenshot-cleaner
  ```
- [ ] Update project board/issues
- [ ] Announce release (if applicable)

## Rollback (If Needed)

If something goes wrong:

1. **Delete the tag:**
   ```bash
   git tag -d v0.1.1
   git push origin :refs/tags/v0.1.1
   ```

2. **Reset version:**
   ```bash
   git reset --hard HEAD~1
   ```

3. **Fix issues and try again**

## Version Strategy

- **Patch** (0.1.0 → 0.1.1): Bug fixes only
- **Minor** (0.1.0 → 0.2.0): New features, backward compatible
- **Major** (0.1.0 → 1.0.0): Breaking changes

## Common Issues

### Tests fail in CI but pass locally
- Check Python version compatibility
- Ensure running on macOS (required)
- Review GitHub Actions logs

### PyPI publish fails
- Verify trusted publisher configured
- Check environment name matches: `pypi`
- Ensure 2FA enabled on PyPI

### Package already exists
- Cannot overwrite versions on PyPI
- Must bump to new version
- Delete tag and re-release

## Resources

- [PUBLISHING.md](PUBLISHING.md) - Detailed publishing guide
- [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md) - Version management
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Development guide
