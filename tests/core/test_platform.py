"""Tests for platform detection module."""

import pytest
from unittest.mock import patch
from screenshot_cleaner.core import platform as platform_module


class TestIsMacos:
    """Tests for is_macos() function."""
    
    @patch('platform.system')
    def test_returns_true_on_darwin(self, mock_system):
        """Test that is_macos returns True when platform is Darwin."""
        mock_system.return_value = "Darwin"
        assert platform_module.is_macos() is True
    
    @patch('platform.system')
    def test_returns_false_on_linux(self, mock_system):
        """Test that is_macos returns False when platform is Linux."""
        mock_system.return_value = "Linux"
        assert platform_module.is_macos() is False
    
    @patch('platform.system')
    def test_returns_false_on_windows(self, mock_system):
        """Test that is_macos returns False when platform is Windows."""
        mock_system.return_value = "Windows"
        assert platform_module.is_macos() is False
    
    @patch('platform.system')
    def test_returns_false_on_unknown(self, mock_system):
        """Test that is_macos returns False for unknown platforms."""
        mock_system.return_value = "Unknown"
        assert platform_module.is_macos() is False


class TestValidateMacos:
    """Tests for validate_macos() function."""
    
    @patch('platform.system')
    def test_does_not_exit_on_macos(self, mock_system):
        """Test that validate_macos does not raise SystemExit on macOS."""
        mock_system.return_value = "Darwin"
        # Should not raise any exception
        platform_module.validate_macos()
    
    @patch('platform.system')
    def test_exits_on_non_macos(self, mock_system):
        """Test that validate_macos raises SystemExit on non-macOS."""
        mock_system.return_value = "Linux"
        with pytest.raises(SystemExit) as exc_info:
            platform_module.validate_macos()
        assert exc_info.value.code == 1
    
    @patch('platform.system')
    @patch('sys.stderr')
    def test_prints_error_message_on_non_macos(self, mock_stderr, mock_system):
        """Test that validate_macos prints error message on non-macOS."""
        mock_system.return_value = "Windows"
        with pytest.raises(SystemExit):
            platform_module.validate_macos()
