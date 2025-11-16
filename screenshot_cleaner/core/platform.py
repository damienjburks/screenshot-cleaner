"""Platform detection and validation for macOS."""

import platform
import sys


def is_macos() -> bool:
    """Check if the current platform is macOS.
    
    Returns:
        bool: True if running on macOS (Darwin), False otherwise.
    """
    return platform.system() == "Darwin"


def validate_macos() -> None:
    """Validate that the current platform is macOS.
    
    Raises:
        SystemExit: If not running on macOS, exits with code 1.
    """
    if not is_macos():
        print("Error: This tool only runs on macOS.", file=sys.stderr)
        sys.exit(1)
