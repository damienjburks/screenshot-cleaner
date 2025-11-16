"""Tests for cleanup module."""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from screenshot_cleaner.core import cleanup


class TestDeleteFile:
    """Tests for delete_file() function."""
    
    def test_deletes_file_successfully(self, tmp_path):
        """Test that file is deleted successfully."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        assert test_file.exists()
        result = cleanup.delete_file(test_file, dry_run=False)
        
        assert result is True
        assert not test_file.exists()
    
    def test_dry_run_does_not_delete(self, tmp_path):
        """Test that dry-run mode doesn't delete files."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        result = cleanup.delete_file(test_file, dry_run=True)
        
        assert result is True
        assert test_file.exists()  # File should still exist
    
    def test_returns_false_on_nonexistent_file(self, tmp_path):
        """Test that deleting nonexistent file returns False."""
        nonexistent = tmp_path / "nonexistent.txt"
        
        result = cleanup.delete_file(nonexistent, dry_run=False)
        
        assert result is False
    
    @patch('os.remove')
    def test_returns_false_on_permission_error(self, mock_remove, tmp_path):
        """Test that permission errors return False."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")
        
        mock_remove.side_effect = PermissionError("Access denied")
        
        result = cleanup.delete_file(test_file, dry_run=False)
        
        assert result is False


class TestDeleteFiles:
    """Tests for delete_files() function."""
    
    def test_deletes_multiple_files(self, tmp_path):
        """Test deleting multiple files successfully."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("content1")
        file2.write_text("content2")
        
        files = [file1, file2]
        success, failure = cleanup.delete_files(files, dry_run=False)
        
        assert success == 2
        assert failure == 0
        assert not file1.exists()
        assert not file2.exists()
    
    def test_dry_run_does_not_delete_files(self, tmp_path):
        """Test that dry-run mode doesn't delete any files."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("content1")
        file2.write_text("content2")
        
        files = [file1, file2]
        success, failure = cleanup.delete_files(files, dry_run=True)
        
        assert success == 2
        assert failure == 0
        assert file1.exists()  # Files should still exist
        assert file2.exists()
    
    def test_handles_mixed_success_and_failure(self, tmp_path):
        """Test handling mix of successful and failed deletions."""
        existing_file = tmp_path / "exists.txt"
        existing_file.write_text("content")
        nonexistent_file = tmp_path / "nonexistent.txt"
        
        files = [existing_file, nonexistent_file]
        success, failure = cleanup.delete_files(files, dry_run=False)
        
        assert success == 1
        assert failure == 1
    
    def test_logs_operations_when_logger_provided(self, tmp_path):
        """Test that operations are logged when logger is provided."""
        mock_logger = MagicMock()
        
        file1 = tmp_path / "file1.txt"
        file1.write_text("content")
        
        files = [file1]
        cleanup.delete_files(files, dry_run=False, logger=mock_logger)
        
        # Verify logger.info was called
        mock_logger.info.assert_called_once()
        assert "Deleted" in str(mock_logger.info.call_args)
    
    def test_logs_dry_run_operations(self, tmp_path):
        """Test that dry-run operations are logged correctly."""
        mock_logger = MagicMock()
        
        file1 = tmp_path / "file1.txt"
        file1.write_text("content")
        
        files = [file1]
        cleanup.delete_files(files, dry_run=True, logger=mock_logger)
        
        # Verify logger.info was called with "Would delete"
        mock_logger.info.assert_called_once()
        assert "Would delete" in str(mock_logger.info.call_args)
    
    def test_logs_failures(self, tmp_path):
        """Test that failures are logged."""
        mock_logger = MagicMock()
        
        nonexistent = tmp_path / "nonexistent.txt"
        
        files = [nonexistent]
        cleanup.delete_files(files, dry_run=False, logger=mock_logger)
        
        # Verify logger.error was called
        mock_logger.error.assert_called_once()
        assert "Failed to delete" in str(mock_logger.error.call_args)
    
    def test_empty_file_list(self):
        """Test handling empty file list."""
        success, failure = cleanup.delete_files([], dry_run=False)
        
        assert success == 0
        assert failure == 0
    
    def test_continues_after_failure(self, tmp_path):
        """Test that deletion continues after individual failures."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "nonexistent.txt"
        file3 = tmp_path / "file3.txt"
        
        file1.write_text("content1")
        file3.write_text("content3")
        
        files = [file1, file2, file3]
        success, failure = cleanup.delete_files(files, dry_run=False)
        
        assert success == 2
        assert failure == 1
        assert not file1.exists()
        assert not file3.exists()
