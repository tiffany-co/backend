"""
Contains the core business logic for database operations (backup, restore, clear).
This module is decoupled from the UI and focuses on executing tasks.
"""

import shlex
import subprocess
from datetime import datetime
from pathlib import Path

import typer
from rich.prompt import Confirm, Prompt

from .config import config  # Import the singleton config instance


class DatabaseManager:
    """Handles the logic for backing up and restoring the database for a specific environment."""

    def __init__(self, env: str):
        self.env = env
        self.compose_file = config.get_compose_file(env)

    def backup(self):
        """Creates a native PostgreSQL backup using pg_dump."""
        config.CONSOLE.print(f"\n[bold yellow]Starting backup for '{self.env}' environment...[/bold yellow]")
        config.BACKUPS_DIR.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename = f"{self.env}-backup-{timestamp}.dump"
        backup_filepath = config.BACKUPS_DIR / backup_filename

        dump_command = (
            f"docker-compose -f {self.compose_file} exec -T db "
            f"pg_dump -U {config.PG_USER} -d {config.PG_DB} -F c -b -v"
        )

        config.CONSOLE.print("Running pg_dump...")
        try:
            with open(backup_filepath, "wb") as f_out:
                self._run_command(dump_command, stdout=f_out)
            config.CONSOLE.print(f"\n[bold green]Success![/bold green] Backup saved to: [cyan]{backup_filepath}[/cyan]")
        except subprocess.CalledProcessError as e:
            config.CONSOLE.print(f"[bold red]Error during pg_dump:[/bold red]")
            config.CONSOLE.print(e.stderr.decode('utf-8', errors='ignore'))
            raise typer.Exit(code=1)

    def restore(self):
        """Restores the database from a user-selected backup file."""
        config.CONSOLE.print(f"\n[bold yellow]Initiating restore for '{self.env}' environment...[/bold yellow]")

        backup_file = self._select_backup_file()
        config.CONSOLE.print(f"\nYou have selected to restore: [bold cyan]{backup_file.name}[/bold cyan]")
        
        if not Confirm.ask(f"[bold red]WARNING:[/bold red] This will WIPE the '{self.env}' database. Are you sure?"):
            config.CONSOLE.print("[yellow]Restore cancelled.[/yellow]")
            raise typer.Exit()

        config.CONSOLE.print(f"\nRestoring from [cyan]{backup_file.name}[/cyan]...")
        
        restore_command = (
            f"docker-compose -f {self.compose_file} exec -T db "
            f"pg_restore -U {config.PG_USER} -d {config.PG_DB} --clean --if-exists"
        )

        try:
            with open(backup_file, "rb") as f_in:
                self._run_command(restore_command, stdin=f_in)
            config.CONSOLE.print("\n[bold green]Success![/bold green] Database restore complete.")
        except subprocess.CalledProcessError as e:
            config.CONSOLE.print(f"[bold red]Error during pg_restore:[/bold red]")
            config.CONSOLE.print(e.stderr.decode('utf-8', errors='ignore'))
            raise typer.Exit(code=1)

    def _select_backup_file(self) -> Path:
        """Finds relevant backup files and prompts the user to choose one."""
        backups = self._get_backup_files()
        config.CONSOLE.print("Available backup files:")
        for i, file in enumerate(backups):
            config.CONSOLE.print(f"  [cyan]{i+1}[/cyan]: {file.name}")
        
        choice = Prompt.ask(
            "\nEnter the number of the backup file to restore", 
            choices=[str(i + 1) for i in range(len(backups))],
            default="1"
        )
        return backups[int(choice) - 1]
    
    def _get_backup_files(self) -> list[Path]:
        """Gets a sorted list of backup files for the current environment."""
        if not config.BACKUPS_DIR.exists() or not any(config.BACKUPS_DIR.iterdir()):
            config.CONSOLE.print(f"[bold red]Error:[/bold red] No backup files found in '{config.BACKUPS_DIR}'.")
            raise typer.Exit(code=1)

        backups = sorted(config.BACKUPS_DIR.glob(f"{self.env}-backup-*.dump"), reverse=True)
        
        if not backups:
            config.CONSOLE.print(f"[bold red]Error:[/bold red] No backups found for the '{self.env}' environment.")
            raise typer.Exit(code=1)
        return backups

    def _run_command(self, command: str, stdin=None, stdout=None):
        """Executes a shell command, handling common errors."""
        try:
            subprocess.run(
                shlex.split(command),
                stdin=stdin,
                stdout=stdout,
                stderr=subprocess.PIPE,
                check=True,
                cwd=config.PROJECT_ROOT
            )
        except FileNotFoundError:
            config.CONSOLE.print(f"[bold red]Error:[/bold red] 'docker-compose' not found. Is Docker installed and in your PATH?")
            raise typer.Exit(code=1)


def clear_backups(force: bool):
    """Deletes all backup files from the backups directory."""
    config.CONSOLE.print(f"\n[bold yellow]Attempting to clear the backups directory: [cyan]{config.BACKUPS_DIR}[/cyan][/bold yellow]")

    if not config.BACKUPS_DIR.exists() or not any(config.BACKUPS_DIR.iterdir()):
        config.CONSOLE.print(f"[bold green]Success![/bold green] The backups directory is already empty or does not exist.")
        raise typer.Exit()

    if not force:
        if not Confirm.ask("[bold red]WARNING:[/bold red] This will permanently delete ALL backup files. Continue?"):
            config.CONSOLE.print("[yellow]Operation cancelled.[/yellow]")
            raise typer.Exit()
    
    deleted_count, error_count = 0, 0
    for item in config.BACKUPS_DIR.iterdir():
        try:
            if item.is_file() and item.name.endswith('.dump'):
                item.unlink()
                deleted_count += 1
        except Exception as e:
            config.CONSOLE.print(f"[bold red]Error deleting {item.name}:[/bold red] {e}")
            error_count += 1
    
    if error_count == 0:
        config.CONSOLE.print(f"\n[bold green]Success![/bold green] Deleted {deleted_count} backup file(s).")
    else:
        config.CONSOLE.print(f"\n[bold yellow]Partial success:[/bold yellow] Deleted {deleted_count} file(s), but {error_count} error(s) occurred.")
        raise typer.Exit(code=1)
