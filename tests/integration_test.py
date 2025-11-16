"""Integration tests for screenshot cleaner.

These tests create real files and test the full workflow.
Run manually with: uv run pytest tests/integration_test.py -v
"""

import os
import time
from pathlib import Path
import pytest

from screenshot_cleaner.core.scanner import find_expired_files
from screenshot_cleaner.core.cleanup import delete_files
from screenshot_cleaner.utils.logging import setup_logger


class TestIntegrationScenarios:
    """Integration tests with real file operations."""
    
    def test_full_workflow_preview_and_clean(self, tmp_path):
        """Test complete workflow: create files, preview, clean."""
        # Create test screenshots with different ages
        old_screenshot1 = tmp_path / "Screen Shot 2024-01-01.png"
        old_screenshot2 = tmp_path / "Screenshot 2024-01-02.png"
        new_screenshot = tmp_path / "Screen Shot 2024-11-15.png"
        non_screenshot = tmp_path / "document.png"
        
        # Write files
        old_screenshot1.write_text("old1")
        old_screenshot2.write_text("old2")
        new_screenshot.write_text("new")
        non_screenshot.write_text("doc")
        
        # Set modification times
        ten_days_ago = time.time() - (10 * 86400)
        os.utime(old_screenshot1, (ten_days_ago, ten_days_ago))
        os.utime(old_screenshot2, (ten_days_ago, ten_days_ago))
        
        # Preview: Find expired files
        expired = find_expired_files(tmp_path, days=7)
        assert len(expired) == 2
        assert old_screenshot1 in expired
        assert old_screenshot2 in expired
        assert new_screenshot not in expired
        assert non_screenshot not in expired
        
        # Clean: Delete expired files
        logger = setup_logger()
        success, failure = delete_files(expired, dry_run=False, logger=logger)
        
        assert success == 2
        assert failure == 0
        assert not old_screenshot1.exists()
        assert not old_screenshot2.exists()
        assert new_screenshot.exists()
        assert non_screenshot.exists()
    
    def test_dry_run_preserves_files(self, tmp_path):
        """Test that dry-run mode doesn't delete files."""
        screenshot = tmp_path / "Screen Shot 2024.png"
        screenshot.write_text("test")
        
        # Make it old
        ten_days_ago = time.time() - (10 * 86400)
        os.utime(screenshot, (ten_days_ago, ten_days_ago))
        
        # Find and "delete" in dry-run mode
        expired = find_expired_files(tmp_path, days=7)
        logger = setup_logger()
        success, failure = delete_files(expired, dry_run=True, logger=logger)
        
        assert success == 1
        assert failure == 0
        assert screenshot.exists()  # File should still exist
    
    def test_custom_days_threshold(self, tmp_path):
        """Test using different age thresholds."""
        screenshot = tmp_path / "Screenshot 2024.png"
        screenshot.write_text("test")
        
        # Make it 5 days old
        five_days_ago = time.time() - (5 * 86400)
        os.utime(screenshot, (five_days_ago, five_days_ago))
        
        # Should not be found with 7 day threshold
        expired_7 = find_expired_files(tmp_path, days=7)
        assert len(expired_7) == 0
        
        # Should be found with 3 day threshold
        expired_3 = find_expired_files(tmp_path, days=3)
        assert len(expired_3) == 1
        
        # Clean with 3 day threshold
        logger = setup_logger()
        success, failure = delete_files(expired_3, dry_run=False, logger=logger)
        
        assert success == 1
        assert not screenshot.exists()
    
    def test_large_directory_performance(self, tmp_path):
        """Test performance with many files."""
        # Create 100 files (mix of screenshots and non-screenshots)
        for i in range(50):
            screenshot = tmp_path / f"Screen Shot {i}.png"
            screenshot.write_text(f"screenshot{i}")
            
            # Make half of them old
            if i < 25:
                ten_days_ago = time.time() - (10 * 86400)
                os.utime(screenshot, (ten_days_ago, ten_days_ago))
        
        for i in range(50):
            other_file = tmp_path / f"document{i}.txt"
            other_file.write_text(f"doc{i}")
        
        # Measure time to find expired files
        start_time = time.time()
        expired = find_expired_files(tmp_path, days=7)
        elapsed = time.time() - start_time
        
        # Should find 25 expired screenshots
        assert len(expired) == 25
        
        # Should complete quickly (< 1 second for 100 files)
        assert elapsed < 1.0
    
    def test_mixed_success_and_failure(self, tmp_path):
        """Test handling of mixed success and failure scenarios."""
        screenshot1 = tmp_path / "Screen Shot 1.png"
        screenshot2 = tmp_path / "Screen Shot 2.png"
        nonexistent = tmp_path / "Screen Shot 3.png"
        
        screenshot1.write_text("test1")
        screenshot2.write_text("test2")
        # Don't create screenshot3
        
        # Try to delete all three
        logger = setup_logger()
        success, failure = delete_files(
            [screenshot1, screenshot2, nonexistent],
            dry_run=False,
            logger=logger
        )
        
        assert success == 2
        assert failure == 1
        assert not screenshot1.exists()
        assert not screenshot2.exists()
    
    def test_log_file_output(self, tmp_path):
        """Test that log file is created and contains expected content."""
        log_file = tmp_path / "test.log"
        screenshot = tmp_path / "Screen Shot 2024.png"
        screenshot.write_text("test")
        
        # Make it old
        ten_days_ago = time.time() - (10 * 86400)
        os.utime(screenshot, (ten_days_ago, ten_days_ago))
        
        # Find and delete with logging
        logger = setup_logger(log_file=log_file)
        expired = find_expired_files(tmp_path, days=7)
        delete_files(expired, dry_run=False, logger=logger)
        
        # Check log file
        assert log_file.exists()
        log_content = log_file.read_text()
        assert "Deleted" in log_content
        assert "Screen Shot 2024.png" in log_content
    
    def test_empty_directory(self, tmp_path):
        """Test handling of empty directory."""
        expired = find_expired_files(tmp_path, days=7)
        assert len(expired) == 0
        
        logger = setup_logger()
        success, failure = delete_files(expired, dry_run=False, logger=logger)
        assert success == 0
        assert failure == 0
    
    def test_no_subdirectory_traversal(self, tmp_path):
        """Test that subdirectories are not scanned."""
        # Create screenshot in main directory
        main_screenshot = tmp_path / "Screen Shot main.png"
        main_screenshot.write_text("main")
        
        # Create subdirectory with screenshot
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        sub_screenshot = subdir / "Screen Shot sub.png"
        sub_screenshot.write_text("sub")
        
        # Make both old
        ten_days_ago = time.time() - (10 * 86400)
        os.utime(main_screenshot, (ten_days_ago, ten_days_ago))
        os.utime(sub_screenshot, (ten_days_ago, ten_days_ago))
        
        # Find expired files
        expired = find_expired_files(tmp_path, days=7)
        
        # Should only find the main directory screenshot
        assert len(expired) == 1
        assert main_screenshot in expired
        assert sub_screenshot not in expired
