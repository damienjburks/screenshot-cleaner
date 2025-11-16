"""CLI interface for screenshot cleaner using Python Fire."""

import sys
from pathlib import Path
from typing import Optional

import fire
from rich.console import Console
from rich.table import Table

from screenshot_cleaner.core.platform import validate_macos
from screenshot_cleaner.core.scanner import get_default_screenshot_dir, find_expired_files
from screenshot_cleaner.core.cleanup import delete_files
from screenshot_cleaner.utils.logging import setup_logger


console = Console()


class ScreenshotCleaner:
    """CLI for cleaning up old screenshot files."""
    
    def preview(
        self,
        path: Optional[str] = None,
        days: int = 7,
        log_file: Optional[str] = None
    ) -> None:
        """Preview screenshots that would be deleted.
        
        Args:
            path: Screenshot directory (default: system screenshot location)
            days: Age threshold in days (default: 7, use 0 for all screenshots)
            log_file: Optional log file path
        """
        # Validate macOS
        validate_macos()
        
        # Validate days parameter
        if days < 0:
            console.print("[red]Error: days must be a non-negative integer[/red]")
            sys.exit(3)
        
        # Setup logger
        log_path = Path(log_file) if log_file else None
        logger = setup_logger(log_file=log_path)
        
        # Determine target directory
        if path:
            target_dir = Path(path)
            if not target_dir.exists():
                console.print(f"[red]Error: Directory does not exist: {target_dir}[/red]")
                sys.exit(2)
            if not target_dir.is_dir():
                console.print(f"[red]Error: Path is not a directory: {target_dir}[/red]")
                sys.exit(2)
        else:
            target_dir = get_default_screenshot_dir()
        
        logger.info(f"Scanning directory: {target_dir}")
        if days == 0:
            logger.info("Looking for all screenshots (no age filter)")
        else:
            logger.info(f"Looking for screenshots older than {days} days")
        
        # Find expired files
        expired_files = find_expired_files(target_dir, days=days)
        
        if not expired_files:
            console.print("[green]No expired screenshots found![/green]")
            logger.info("No expired screenshots found")
            return
        
        # Display results in a table
        title = "All screenshots" if days == 0 else f"Screenshots older than {days} days"
        table = Table(title=title)
        table.add_column("File", style="cyan")
        table.add_column("Age (days)", style="yellow")
        
        from screenshot_cleaner.core.scanner import get_file_age_days
        for file_path in expired_files:
            age = get_file_age_days(file_path)
            table.add_row(str(file_path), str(age))
        
        console.print(table)
        console.print(f"\n[yellow]Total: {len(expired_files)} file(s) would be deleted[/yellow]")
        logger.info(f"Found {len(expired_files)} expired screenshot(s)")
    
    def clean(
        self,
        path: Optional[str] = None,
        days: int = 7,
        force: bool = False,
        dry_run: bool = False,
        log_file: Optional[str] = None
    ) -> None:
        """Delete old screenshots.
        
        Args:
            path: Screenshot directory (default: system screenshot location)
            days: Age threshold in days (default: 7, use 0 for all screenshots)
            force: Skip confirmation prompt
            dry_run: Preview only, don't delete
            log_file: Optional log file path
        """
        # Validate macOS
        validate_macos()
        
        # Validate days parameter
        if days < 0:
            console.print("[red]Error: days must be a non-negative integer[/red]")
            sys.exit(3)
        
        # Setup logger
        log_path = Path(log_file) if log_file else None
        logger = setup_logger(log_file=log_path)
        
        # Determine target directory
        if path:
            target_dir = Path(path)
            if not target_dir.exists():
                console.print(f"[red]Error: Directory does not exist: {target_dir}[/red]")
                sys.exit(2)
            if not target_dir.is_dir():
                console.print(f"[red]Error: Path is not a directory: {target_dir}[/red]")
                sys.exit(2)
        else:
            target_dir = get_default_screenshot_dir()
        
        logger.info(f"Scanning directory: {target_dir}")
        if days == 0:
            logger.info("Looking for all screenshots (no age filter)")
        else:
            logger.info(f"Looking for screenshots older than {days} days")
        
        # Find expired files
        expired_files = find_expired_files(target_dir, days=days)
        
        if not expired_files:
            console.print("[green]No expired screenshots found![/green]")
            logger.info("No expired screenshots found")
            return
        
        # Display what will be deleted
        console.print(f"[yellow]Found {len(expired_files)} expired screenshot(s)[/yellow]")
        
        if dry_run:
            console.print("[cyan]DRY RUN MODE - No files will be deleted[/cyan]")
        
        # Show preview
        table = Table(title=f"Screenshots to {'preview' if dry_run else 'delete'}")
        table.add_column("File", style="cyan")
        
        for file_path in expired_files[:10]:  # Show first 10
            table.add_row(str(file_path))
        
        if len(expired_files) > 10:
            table.add_row(f"... and {len(expired_files) - 10} more")
        
        console.print(table)
        
        # Ask for confirmation unless force mode or dry run
        if not force and not dry_run:
            response = input(f"\nDelete {len(expired_files)} file(s)? (y/N): ")
            if response.lower() != 'y':
                console.print("[yellow]Operation cancelled[/yellow]")
                logger.info("Operation cancelled by user")
                return
        
        # Perform deletion
        success_count, failure_count = delete_files(
            expired_files,
            dry_run=dry_run,
            logger=logger
        )
        
        # Report results
        if dry_run:
            console.print(f"[green]Would delete {success_count} file(s)[/green]")
        else:
            console.print(f"[green]Successfully deleted {success_count} file(s)[/green]")
            if failure_count > 0:
                console.print(f"[red]Failed to delete {failure_count} file(s)[/red]")
        
        logger.info(f"Operation complete: {success_count} success, {failure_count} failures")


def main():
    """Entry point for the CLI."""
    fire.Fire(ScreenshotCleaner)


if __name__ == "__main__":
    main()
