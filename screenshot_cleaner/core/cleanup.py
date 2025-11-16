"""File deletion operations with dry-run support."""

import os
from pathlib import Path
from typing import Optional
from logging import Logger


def delete_file(file_path: Path, dry_run: bool = False) -> bool:
    """Delete a single file.
    
    Args:
        file_path: Path to the file to delete.
        dry_run: If True, don't actually delete (default: False).
    
    Returns:
        bool: True if successful (or would be in dry-run), False otherwise.
    """
    if dry_run:
        # In dry-run mode, just return True without deleting
        return True
    
    try:
        os.remove(file_path)
        return True
    except (OSError, PermissionError):
        return False


def delete_files(
    files: list[Path],
    dry_run: bool = False,
    logger: Optional[Logger] = None
) -> tuple[int, int]:
    """Delete multiple files.
    
    Args:
        files: List of file paths to delete.
        dry_run: If True, don't actually delete (default: False).
        logger: Optional logger instance for logging operations.
    
    Returns:
        tuple[int, int]: (success_count, failure_count)
    """
    success_count = 0
    failure_count = 0
    
    for file_path in files:
        success = delete_file(file_path, dry_run=dry_run)
        
        if success:
            success_count += 1
            if logger:
                action = "Would delete" if dry_run else "Deleted"
                logger.info(f"{action}: {file_path}")
        else:
            failure_count += 1
            if logger:
                logger.error(f"Failed to delete: {file_path}")
    
    return success_count, failure_count
