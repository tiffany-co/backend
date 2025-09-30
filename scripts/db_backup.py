"""
This script serves as the command-line interface (CLI) entry point for
managing database backups. It uses Typer to define commands and delegates
the actual work to the DatabaseManager and helper functions.
"""

from typing_extensions import Annotated
import typer

# The new structure requires importing from the sub-directory
from backup_utils.manager import DatabaseManager, clear_backups

app = typer.Typer(
    help="A utility for creating, restoring, and clearing native PostgreSQL database backups.",
    add_completion=False
)

@app.command()
def backup(
    env: Annotated[str, typer.Option(..., "--env", "-e", help="The environment to back up ('dev' or 'prod').")]
):
    """Creates a native PostgreSQL backup using pg_dump."""
    manager = DatabaseManager(env=env)
    manager.backup()

@app.command()
def restore(
    env: Annotated[str, typer.Option(..., "--env", "-e", help="The environment to restore ('dev' or 'prod').")]
):
    """Restores the database from a backup file."""
    manager = DatabaseManager(env=env)
    manager.restore()

@app.command()
def clear(
    force: Annotated[bool, typer.Option("--force", "-f", help="Force deletion without confirmation.")] = False
):
    """Deletes all backup files from the backups directory."""
    clear_backups(force=force)

if __name__ == "__main__":
    app()

