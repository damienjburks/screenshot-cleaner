"""Tests for CLI module."""

import os
import time
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from screenshot_cleaner.cli import ScreenshotCleaner


class TestPreviewCommand:
    """Tests for preview command."""
    
    @patch('screenshot_cleaner.cli.validate_macos')
    @patch('screenshot_cleaner.cli.find_expired_files')
    def test_preview_with_no_expired_files(self, mock_find, mock_validate, capsys):
        """Test preview when no expired files found."""
        mock_find.return_value = []
        
        cli = ScreenshotCleaner()
        cli.preview()
        
        captured = capsys.readouterr()
        assert "No expired screenshots found" in captured.out
    
    @patch('screenshot_cleaner.cli.validate_macos')
    @patch('screenshot_cleaner.cli.find_expired_files')
    @patch('screenshot_cleaner.core.scanner.get_file_age_days')
    def test_preview_displays_expired_files(self, mock_age, mock_find, mock_validate, tmp_path, capsys):
        """Test preview displays expired files in table."""
        test_file = tmp_path / "Screen Shot 2024.png"
        test_file.write_text("test")
        
        mock_find.return_value = [test_file]
        mock_age.return_value = 10
        
        cli = ScreenshotCleaner()
        cli.preview(path=str(tmp_path))
        
        captured = capsys.readouterr()
        # File path may be wrapped in table, so check for key parts
        assert "Shot 2024.png" in captured.out
        assert "1 file(s) would be deleted" in captured.out
    
    @patch('screenshot_cleaner.cli.validate_macos')
    def test_preview_with_invalid_directory(self, mock_validate):
        """Test preview with nonexistent directory."""
        cli = ScreenshotCleaner()
        
        with pytest.raises(SystemExit) as exc_info:
            cli.preview(path="/nonexistent/directory")
        
        assert exc_info.value.code == 2
    
    @patch('screenshot_cleaner.cli.validate_macos')
    def test_preview_with_invalid_days(self, mock_validate):
        """Test preview with invalid days parameter."""
        cli = ScreenshotCleaner()
        
        with pytest.raises(SystemExit) as exc_info:
            cli.preview(days=-1)
        
        assert exc_info.value.code == 3
    
    @patch('screenshot_cleaner.cli.validate_macos')
    @patch('screenshot_cleaner.cli.find_expired_files')
    def test_preview_with_custom_days(self, mock_find, mock_validate, tmp_path):
        """Test preview with custom days threshold."""
        mock_find.return_value = []
        
        cli = ScreenshotCleaner()
        cli.preview(path=str(tmp_path), days=14)
        
        # Verify find_expired_files was called with correct days
        mock_find.assert_called_once()
        assert mock_find.call_args[1]['days'] == 14
    
    @patch('screenshot_cleaner.cli.validate_macos')
    @patch('screenshot_cleaner.cli.find_expired_files')
    @patch('screenshot_cleaner.core.scanner.get_file_age_days')
    def test_preview_with_zero_days(self, mock_age, mock_find, mock_validate, tmp_path, capsys):
        """Test preview with days=0 to show all screenshots."""
        test_file = tmp_path / "Screen Shot 2024.png"
        test_file.write_text("test")
        
        mock_find.return_value = [test_file]
        mock_age.return_value = 0
        
        cli = ScreenshotCleaner()
        cli.preview(path=str(tmp_path), days=0)
        
        captured = capsys.readouterr()
        assert "All screenshots" in captured.out or "Shot 2024.png" in captured.out
        assert "1 file(s) would be deleted" in captured.out


class TestCleanCommand:
    """Tests for clean command."""
    
    @patch('screenshot_cleaner.cli.validate_macos')
    @patch('screenshot_cleaner.cli.find_expired_files')
    def test_clean_with_no_expired_files(self, mock_find, mock_validate, capsys):
        """Test clean when no expired files found."""
        mock_find.return_value = []
        
        cli = ScreenshotCleaner()
        cli.clean(force=True)
        
        captured = capsys.readouterr()
        assert "No expired screenshots found" in captured.out
    
    @patch('screenshot_cleaner.cli.validate_macos')
    @patch('screenshot_cleaner.cli.find_expired_files')
    @patch('screenshot_cleaner.cli.delete_files')
    def test_clean_with_force_flag(self, mock_delete, mock_find, mock_validate, tmp_path, capsys):
        """Test clean with force flag skips confirmation."""
        test_file = tmp_path / "Screen Shot 2024.png"
        test_file.write_text("test")
        
        mock_find.return_value = [test_file]
        mock_delete.return_value = (1, 0)  # 1 success, 0 failures
        
        cli = ScreenshotCleaner()
        cli.clean(path=str(tmp_path), force=True)
        
        # Verify delete_files was called
        mock_delete.assert_called_once()
        
        captured = capsys.readouterr()
        assert "Successfully deleted 1 file(s)" in captured.out
    
    @patch('screenshot_cleaner.cli.validate_macos')
    @patch('screenshot_cleaner.cli.find_expired_files')
    @patch('screenshot_cleaner.cli.delete_files')
    def test_clean_with_dry_run(self, mock_delete, mock_find, mock_validate, tmp_path, capsys):
        """Test clean with dry-run flag."""
        test_file = tmp_path / "Screen Shot 2024.png"
        test_file.write_text("test")
        
        mock_find.return_value = [test_file]
        mock_delete.return_value = (1, 0)
        
        cli = ScreenshotCleaner()
        cli.clean(path=str(tmp_path), dry_run=True)
        
        # Verify delete_files was called with dry_run=True
        mock_delete.assert_called_once()
        assert mock_delete.call_args[1]['dry_run'] is True
        
        captured = capsys.readouterr()
        assert "DRY RUN MODE" in captured.out
        assert "Would delete 1 file(s)" in captured.out
    
    @patch('screenshot_cleaner.cli.validate_macos')
    @patch('screenshot_cleaner.cli.find_expired_files')
    @patch('builtins.input')
    def test_clean_with_confirmation_declined(self, mock_input, mock_find, mock_validate, tmp_path, capsys):
        """Test clean when user declines confirmation."""
        test_file = tmp_path / "Screen Shot 2024.png"
        test_file.write_text("test")
        
        mock_find.return_value = [test_file]
        mock_input.return_value = 'n'
        
        cli = ScreenshotCleaner()
        cli.clean(path=str(tmp_path))
        
        captured = capsys.readouterr()
        assert "Operation cancelled" in captured.out
    
    @patch('screenshot_cleaner.cli.validate_macos')
    @patch('screenshot_cleaner.cli.find_expired_files')
    @patch('screenshot_cleaner.cli.delete_files')
    @patch('builtins.input')
    def test_clean_with_confirmation_accepted(self, mock_input, mock_delete, mock_find, mock_validate, tmp_path, capsys):
        """Test clean when user accepts confirmation."""
        test_file = tmp_path / "Screen Shot 2024.png"
        test_file.write_text("test")
        
        mock_find.return_value = [test_file]
        mock_delete.return_value = (1, 0)
        mock_input.return_value = 'y'
        
        cli = ScreenshotCleaner()
        cli.clean(path=str(tmp_path))
        
        # Verify delete_files was called
        mock_delete.assert_called_once()
        
        captured = capsys.readouterr()
        assert "Successfully deleted 1 file(s)" in captured.out
    
    @patch('screenshot_cleaner.cli.validate_macos')
    @patch('screenshot_cleaner.cli.find_expired_files')
    @patch('screenshot_cleaner.cli.delete_files')
    def test_clean_reports_failures(self, mock_delete, mock_find, mock_validate, tmp_path, capsys):
        """Test clean reports deletion failures."""
        test_file = tmp_path / "Screen Shot 2024.png"
        test_file.write_text("test")
        
        mock_find.return_value = [test_file]
        mock_delete.return_value = (1, 2)  # 1 success, 2 failures
        
        cli = ScreenshotCleaner()
        cli.clean(path=str(tmp_path), force=True)
        
        captured = capsys.readouterr()
        assert "Successfully deleted 1 file(s)" in captured.out
        assert "Failed to delete 2 file(s)" in captured.out
    
    @patch('screenshot_cleaner.cli.validate_macos')
    def test_clean_with_invalid_directory(self, mock_validate):
        """Test clean with nonexistent directory."""
        cli = ScreenshotCleaner()
        
        with pytest.raises(SystemExit) as exc_info:
            cli.clean(path="/nonexistent/directory", force=True)
        
        assert exc_info.value.code == 2
    
    @patch('screenshot_cleaner.cli.validate_macos')
    def test_clean_with_invalid_days(self, mock_validate):
        """Test clean with invalid days parameter."""
        cli = ScreenshotCleaner()
        
        with pytest.raises(SystemExit) as exc_info:
            cli.clean(days=-1, force=True)
        
        assert exc_info.value.code == 3


class TestMacOSValidation:
    """Tests for macOS validation in CLI."""
    
    @patch('screenshot_cleaner.cli.validate_macos')
    def test_preview_validates_macos(self, mock_validate):
        """Test that preview validates macOS."""
        mock_validate.side_effect = SystemExit(1)
        
        cli = ScreenshotCleaner()
        
        with pytest.raises(SystemExit):
            cli.preview()
        
        mock_validate.assert_called_once()
    
    @patch('screenshot_cleaner.cli.validate_macos')
    def test_clean_validates_macos(self, mock_validate):
        """Test that clean validates macOS."""
        mock_validate.side_effect = SystemExit(1)
        
        cli = ScreenshotCleaner()
        
        with pytest.raises(SystemExit):
            cli.clean(force=True)
        
        mock_validate.assert_called_once()
