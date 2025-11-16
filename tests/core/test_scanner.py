"""Tests for scanner module."""

import os
import time
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from screenshot_cleaner.core import scanner


class TestGetDefaultScreenshotDir:
    """Tests for get_default_screenshot_dir() function."""
    
    def test_returns_desktop_path(self):
        """Test that default directory is ~/Desktop."""
        result = scanner.get_default_screenshot_dir()
        expected = Path.home() / "Desktop"
        assert result == expected


class TestMatchesScreenshotPattern:
    """Tests for matches_screenshot_pattern() function."""
    
    def test_matches_screen_shot_pattern(self):
        """Test matching 'Screen Shot' pattern."""
        assert scanner.matches_screenshot_pattern("Screen Shot 2024-01-01 at 10.00.00 AM.png") is True
    
    def test_matches_screenshot_pattern(self):
        """Test matching 'Screenshot' pattern."""
        assert scanner.matches_screenshot_pattern("Screenshot 2024-01-01.png") is True
    
    def test_matches_case_insensitive(self):
        """Test that matching is case-insensitive."""
        assert scanner.matches_screenshot_pattern("screen shot 2024.png") is True
        assert scanner.matches_screenshot_pattern("SCREEN SHOT 2024.png") is True
        assert scanner.matches_screenshot_pattern("screenshot 2024.png") is True
        assert scanner.matches_screenshot_pattern("SCREENSHOT 2024.png") is True
    
    def test_does_not_match_non_screenshot(self):
        """Test that non-screenshot files don't match."""
        assert scanner.matches_screenshot_pattern("document.png") is False
        assert scanner.matches_screenshot_pattern("photo.jpg") is False
        assert scanner.matches_screenshot_pattern("image.png") is False
    
    def test_does_not_match_wrong_extension(self):
        """Test that files with wrong extension don't match."""
        assert scanner.matches_screenshot_pattern("Screen Shot 2024.jpg") is False
        assert scanner.matches_screenshot_pattern("Screenshot 2024.pdf") is False


class TestGetFileAgeDays:
    """Tests for get_file_age_days() function."""
    
    def test_calculates_age_correctly(self, tmp_path):
        """Test that file age is calculated correctly."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")
        
        # Set modification time to 10 days ago
        ten_days_ago = time.time() - (10 * 86400)
        os.utime(test_file, (ten_days_ago, ten_days_ago))
        
        age = scanner.get_file_age_days(test_file)
        assert age == 10
    
    def test_new_file_has_zero_age(self, tmp_path):
        """Test that newly created file has age 0."""
        test_file = tmp_path / "new.txt"
        test_file.write_text("new")
        
        age = scanner.get_file_age_days(test_file)
        assert age == 0


class TestFindExpiredFiles:
    """Tests for find_expired_files() function."""
    
    def test_finds_expired_screenshots(self, tmp_path):
        """Test finding expired screenshot files."""
        # Create old screenshot
        old_screenshot = tmp_path / "Screen Shot 2024-01-01.png"
        old_screenshot.write_text("old")
        ten_days_ago = time.time() - (10 * 86400)
        os.utime(old_screenshot, (ten_days_ago, ten_days_ago))
        
        # Create new screenshot
        new_screenshot = tmp_path / "Screen Shot 2024-01-15.png"
        new_screenshot.write_text("new")
        
        # Find files older than 7 days
        expired = scanner.find_expired_files(tmp_path, days=7)
        
        assert len(expired) == 1
        assert expired[0] == old_screenshot
    
    def test_ignores_non_screenshot_files(self, tmp_path):
        """Test that non-screenshot files are ignored."""
        # Create old non-screenshot file
        old_file = tmp_path / "document.png"
        old_file.write_text("old")
        ten_days_ago = time.time() - (10 * 86400)
        os.utime(old_file, (ten_days_ago, ten_days_ago))
        
        expired = scanner.find_expired_files(tmp_path, days=7)
        
        assert len(expired) == 0
    
    def test_no_subdirectory_traversal(self, tmp_path):
        """Test that subdirectories are not traversed."""
        # Create subdirectory with old screenshot
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        old_screenshot = subdir / "Screen Shot 2024-01-01.png"
        old_screenshot.write_text("old")
        ten_days_ago = time.time() - (10 * 86400)
        os.utime(old_screenshot, (ten_days_ago, ten_days_ago))
        
        # Find expired files in parent directory
        expired = scanner.find_expired_files(tmp_path, days=7)
        
        # Should not find the file in subdirectory
        assert len(expired) == 0
    
    def test_returns_empty_list_for_nonexistent_directory(self):
        """Test that nonexistent directory returns empty list."""
        nonexistent = Path("/nonexistent/directory")
        expired = scanner.find_expired_files(nonexistent, days=7)
        
        assert expired == []
    
    def test_returns_empty_list_for_file_path(self, tmp_path):
        """Test that passing a file path returns empty list."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")
        
        expired = scanner.find_expired_files(test_file, days=7)
        
        assert expired == []
    
    def test_handles_permission_errors_gracefully(self, tmp_path, monkeypatch):
        """Test that permission errors are handled gracefully."""
        # Mock os.scandir to raise PermissionError
        def mock_scandir(path):
            raise PermissionError("Access denied")
        
        monkeypatch.setattr(os, 'scandir', mock_scandir)
        
        expired = scanner.find_expired_files(tmp_path, days=7)
        
        assert expired == []
    
    def test_custom_days_threshold(self, tmp_path):
        """Test using custom days threshold."""
        # Create screenshot 5 days old
        screenshot = tmp_path / "Screenshot 2024.png"
        screenshot.write_text("test")
        five_days_ago = time.time() - (5 * 86400)
        os.utime(screenshot, (five_days_ago, five_days_ago))
        
        # Should not be found with 7 day threshold
        expired_7 = scanner.find_expired_files(tmp_path, days=7)
        assert len(expired_7) == 0
        
        # Should be found with 3 day threshold
        expired_3 = scanner.find_expired_files(tmp_path, days=3)
        assert len(expired_3) == 1
