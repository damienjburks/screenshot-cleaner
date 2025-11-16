#!/bin/bash
# Release script for Screenshot Cleaner
# Usage: ./scripts/release.sh [patch|minor|major]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if version type is provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Version type required${NC}"
    echo "Usage: ./scripts/release.sh [patch|minor|major]"
    exit 1
fi

VERSION_TYPE=$1

# Validate version type
if [[ ! "$VERSION_TYPE" =~ ^(patch|minor|major)$ ]]; then
    echo -e "${RED}Error: Invalid version type${NC}"
    echo "Must be one of: patch, minor, major"
    exit 1
fi

echo -e "${YELLOW}Starting release process for ${VERSION_TYPE} version...${NC}"

# Check if working directory is clean
if [[ -n $(git status -s) ]]; then
    echo -e "${RED}Error: Working directory is not clean${NC}"
    echo "Please commit or stash your changes first"
    git status -s
    exit 1
fi

# Run tests
echo -e "${YELLOW}Running tests...${NC}"
uv run pytest --cov=screenshot_cleaner --cov-report=term

# Check coverage
COVERAGE=$(uv run pytest --cov=screenshot_cleaner --cov-report=term | grep "TOTAL" | awk '{print $4}' | sed 's/%//')
if [ "${COVERAGE%.*}" -lt 90 ]; then
    echo -e "${RED}Error: Coverage is below 90% (${COVERAGE}%)${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Tests passed with ${COVERAGE}% coverage${NC}"

# Show current version
CURRENT_VERSION=$(uv run bump-my-version show current_version)
echo -e "${YELLOW}Current version: ${CURRENT_VERSION}${NC}"

# Preview version bump
echo -e "${YELLOW}Preview of version bump:${NC}"
uv run bump-my-version bump $VERSION_TYPE --dry-run --allow-dirty

# Confirm
read -p "Proceed with version bump? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Release cancelled${NC}"
    exit 0
fi

# Bump version
echo -e "${YELLOW}Bumping version...${NC}"
uv run bump-my-version bump $VERSION_TYPE

NEW_VERSION=$(uv run bump-my-version show current_version)
echo -e "${GREEN}✓ Version bumped to ${NEW_VERSION}${NC}"

# Push changes
echo -e "${YELLOW}Pushing changes and tags...${NC}"
git push
git push --tags

echo -e "${GREEN}✓ Release complete!${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Create a GitHub release from tag v${NEW_VERSION}"
echo "2. Copy CHANGELOG entry to release notes"
echo "3. Publish to PyPI if desired"
