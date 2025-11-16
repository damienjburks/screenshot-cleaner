"""Shared pytest fixtures and configuration."""

import pytest


@pytest.fixture
def mock_logger(mocker):
    """Provide a mock logger for testing."""
    return mocker.MagicMock()
