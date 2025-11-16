"""Tests for logging module."""

import logging
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from screenshot_cleaner.utils import logging as log_module


class TestSetupLogger:
    """Tests for setup_logger() function."""
    
    def test_creates_logger_with_stdout_handler(self):
        """Test that logger is created with stdout handler."""
        logger = log_module.setup_logger()
        
        assert logger.name == "screenshot_cleaner"
        assert logger.level == logging.INFO
        assert len(logger.handlers) >= 1
        
        # Check that at least one handler is a StreamHandler
        has_stream_handler = any(
            isinstance(h, logging.StreamHandler) for h in logger.handlers
        )
        assert has_stream_handler
    
    def test_creates_logger_with_file_handler(self, tmp_path):
        """Test that logger is created with file handler when log_file specified."""
        log_file = tmp_path / "test.log"
        logger = log_module.setup_logger(log_file=log_file)
        
        # Should have both stdout and file handlers
        assert len(logger.handlers) >= 2
        
        # Check that at least one handler is a FileHandler
        has_file_handler = any(
            isinstance(h, logging.FileHandler) for h in logger.handlers
        )
        assert has_file_handler
    
    def test_clears_existing_handlers(self):
        """Test that existing handlers are cleared."""
        # Setup logger first time
        logger1 = log_module.setup_logger()
        handler_count_1 = len(logger1.handlers)
        
        # Setup logger second time
        logger2 = log_module.setup_logger()
        handler_count_2 = len(logger2.handlers)
        
        # Should have same number of handlers (not doubled)
        assert handler_count_2 == handler_count_1
    
    def test_formatter_includes_timestamp(self):
        """Test that log formatter includes timestamp."""
        logger = log_module.setup_logger()
        
        # Check formatter format string
        for handler in logger.handlers:
            formatter = handler.formatter
            assert formatter is not None
            assert '%(asctime)s' in formatter._fmt
            assert '%(levelname)s' in formatter._fmt
            assert '%(message)s' in formatter._fmt


class TestLogInfo:
    """Tests for log_info() function."""
    
    @patch('logging.Logger.info')
    def test_logs_info_message(self, mock_info):
        """Test that info messages are logged."""
        # Setup logger first
        log_module.setup_logger()
        
        log_module.log_info("Test message")
        
        mock_info.assert_called_once_with("Test message")


class TestLogError:
    """Tests for log_error() function."""
    
    @patch('logging.Logger.error')
    def test_logs_error_message(self, mock_error):
        """Test that error messages are logged."""
        # Setup logger first
        log_module.setup_logger()
        
        log_module.log_error("Error message")
        
        mock_error.assert_called_once_with("Error message")


class TestLogFileOperation:
    """Tests for log_file_operation() function."""
    
    @patch('logging.Logger.info')
    def test_logs_successful_operation(self, mock_info, tmp_path):
        """Test logging successful file operation."""
        # Setup logger first
        log_module.setup_logger()
        
        test_file = tmp_path / "test.txt"
        log_module.log_file_operation(test_file, "Delete", success=True)
        
        mock_info.assert_called_once()
        call_args = str(mock_info.call_args)
        assert "Delete" in call_args
        assert str(test_file) in call_args
    
    @patch('logging.Logger.error')
    def test_logs_failed_operation(self, mock_error, tmp_path):
        """Test logging failed file operation."""
        # Setup logger first
        log_module.setup_logger()
        
        test_file = tmp_path / "test.txt"
        log_module.log_file_operation(test_file, "Delete", success=False)
        
        mock_error.assert_called_once()
        call_args = str(mock_error.call_args)
        assert "Failed" in call_args
        assert str(test_file) in call_args


class TestLoggerIntegration:
    """Integration tests for logging functionality."""
    
    def test_logs_to_file(self, tmp_path):
        """Test that logs are written to file."""
        log_file = tmp_path / "test.log"
        logger = log_module.setup_logger(log_file=log_file)
        
        logger.info("Test log message")
        
        # Check that log file was created and contains message
        assert log_file.exists()
        content = log_file.read_text()
        assert "Test log message" in content
        assert "INFO" in content
    
    def test_log_format(self, tmp_path, caplog):
        """Test that log messages have correct format."""
        logger = log_module.setup_logger()
        
        with caplog.at_level(logging.INFO):
            logger.info("Formatted message")
        
        # Check that log record has expected format
        assert len(caplog.records) == 1
        record = caplog.records[0]
        assert record.levelname == "INFO"
        assert record.message == "Formatted message"
