"""Logging utilities for screenshot cleaner."""

import logging
import sys
from pathlib import Path
from typing import Optional
from rich.console import Console


# Global console for Rich output
console = Console()


def setup_logger(log_file: Optional[Path] = None) -> logging.Logger:
    """Configure and return a logger instance.
    
    Args:
        log_file: Optional path to log file for file output.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("screenshot_cleaner")
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create formatter with timestamp
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
    
    # Always add stdout handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)
    
    # Add file handler if log_file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def log_info(message: str) -> None:
    """Log an info-level message.
    
    Args:
        message: The message to log.
    """
    logger = logging.getLogger("screenshot_cleaner")
    logger.info(message)


def log_error(message: str) -> None:
    """Log an error-level message.
    
    Args:
        message: The error message to log.
    """
    logger = logging.getLogger("screenshot_cleaner")
    logger.error(message)


def log_file_operation(file_path: Path, operation: str, success: bool) -> None:
    """Log a file operation with status.
    
    Args:
        file_path: Path to the file being operated on.
        operation: Description of the operation (e.g., "delete", "would delete").
        success: Whether the operation was successful.
    """
    logger = logging.getLogger("screenshot_cleaner")
    
    if success:
        logger.info(f"{operation}: {file_path}")
    else:
        logger.error(f"Failed to {operation.lower()}: {file_path}")
