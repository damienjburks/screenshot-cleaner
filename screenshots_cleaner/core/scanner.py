"""Screenshot file discovery and filtering."""

import os
import re
import time
from pathlib import Path


def get_default_screenshot_dir() -> Path:
    """Get the default macOS screenshot directory.
    
    Returns:
        Path: The default screenshot directory (typically ~/Desktop).
    """
    return Path.home() / "Desktop"


def matches_screenshot_pattern(filename: str) -> bool:
    """Check if filename matches common macOS screenshot patterns.
    
    Matches patterns like:
    - Screen Shot 2024-01-01 at 10.00.00 AM.png
    - Screenshot 2024-01-01.png
    
    Args:
        filename: The filename to check.
    
    Returns:
        bool: True if filename matches screenshot pattern, False otherwise.
    """
    # Case-insensitive patterns for common macOS screenshot names
    patterns = [
        r"^screen shot .+\.png$",
        r"^screenshot .+\.png$",
    ]
    
    filename_lower = filename.lower()
    return any(re.match(pattern, filename_lower) for pattern in patterns)


def get_file_age_days(file_path: Path) -> int:
    """Calculate file age in days based on modification time.
    
    Args:
        file_path: Path to the file.
    
    Returns:
        int: Age of the file in days.
    """
    mtime = os.path.getmtime(file_path)
    current_time = time.time()
    age_seconds = current_time - mtime
    age_days = int(age_seconds / 86400)  # 86400 seconds in a day
    return age_days


def find_expired_files(directory: Path, days: int = 7) -> list[Path]:
    """Find all expired screenshot files in the directory.
    
    Only scans files directly in the directory (no subdirectory traversal).
    
    Args:
        directory: The directory to scan for screenshots.
        days: Age threshold in days (default: 7).
    
    Returns:
        list[Path]: List of expired screenshot file paths.
    """
    if not directory.exists():
        return []
    
    if not directory.is_dir():
        return []
    
    expired_files = []
    
    try:
        # Use os.scandir for efficient directory listing
        with os.scandir(directory) as entries:
            for entry in entries:
                # Only process files (not directories)
                if not entry.is_file(follow_symlinks=False):
                    continue
                
                # Check if filename matches screenshot pattern
                if not matches_screenshot_pattern(entry.name):
                    continue
                
                # Check if file is old enough
                file_path = Path(entry.path)
                try:
                    file_age = get_file_age_days(file_path)
                    if file_age >= days:
                        expired_files.append(file_path)
                except (OSError, PermissionError):
                    # Skip files we can't access
                    continue
    
    except (OSError, PermissionError):
        # Return empty list if we can't access the directory
        return []
    
    return expired_files
