import os
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing_extensions import Annotated

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Confirm, Prompt

# --- Initial Setup ---
console = Console()
app = typer.Typer()

# This script is run from within the 'backend' directory via `poetry -C backend run ...`
# Therefore, the backend root is the script's parent's parent.
BACKEND_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_ROOT.parent

# Add the backend root to the Python path to allow module imports (e.g., from app.core)
sys.path.insert(0, str(BACKEND_ROOT))

# Load environment variables from the root .env file in CaptainDock
env_path = PROJECT_ROOT / ".env"
if not env_path.exists():
    console.print(f"[bold red]Error:[/bold red] '.env' file not found at '{env_path}'. Please create one from '.env.example'.")
    raise typer.Exit(code=1)
load_dotenv(dotenv_path=env_path)

class DatabaseManager:
    """Handles the logic for backing up and restoring the database."""

    def __init__(self, env: str):
        self.env = env
        self.console = console
        self.backups_dir = PROJECT_ROOT / "backups"
        self.pg_user, self.pg_db = self._get_db_credentials()
        self.compose_file = self._get_compose_file()

    def _get_db_credentials(self) -> tuple[str, str]:
        """Gets and validates required database credentials from environment variables."""
        pg_user = os.getenv("POSTGRES_USER")
        pg_db = os.getenv("POSTGRES_DB")
        if not all([pg_user, pg_db]):
            self.console.print("[bold red]Error:[/bold red] Required environment variables (POSTGRES_USER, POSTGRES_DB) are not set.")
            raise typer.Exit(code=1)
        return pg_user, pg_db

    def _get_compose_file(self) -> str:
        """Gets the correct docker-compose file path for the environment."""
        compose_files = {
            "dev": "docker-compose.dev.yml",
            "prod": "docker-compose.prod.yml",
        }
        file_name = compose_files.get(self.env)
        if not file_name:
            self.console.print(f"[bold red]Error:[/bold red] Invalid environment '{self.env}'. Choose 'dev' or 'prod'.")
            raise typer.Exit(code=1)
        return file_name

    def backup(self):
        """Creates a native PostgreSQL backup using pg_dump."""
        self.console.print(f"\n[bold yellow]Starting backup for '{self.env}' environment...[/bold yellow]")
        self.backups_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename = f"{self.env}-backup-{timestamp}.dump"
        backup_filepath = self.backups_dir / backup_filename

        dump_command = (
            f"docker-compose -f {self.compose_file} exec -T db "
            f"pg_dump -U {self.pg_user} -d {self.pg_db} -F c -b -v"
        )

        self.console.print("Running pg_dump...")
        try:
            with open(backup_filepath, "wb") as f_out:
                subprocess.run(
                    shlex.split(dump_command),
                    stdout=f_out,
                    stderr=subprocess.PIPE,
                    check=True,
                    cwd=PROJECT_ROOT  # Explicitly set the working directory to CaptainDock root
                )
            self.console.print(f"\n[bold green]Success![/bold green] Backup saved to: [cyan]{backup_filepath}[/cyan]")
        except subprocess.CalledProcessError as e:
            self.console.print(f"[bold red]Error during pg_dump:[/bold red]")
            self.console.print(e.stderr.decode('utf-8'))
            raise typer.Exit(code=1)
        except FileNotFoundError:
            self.console.print(f"[bold red]Error:[/bold red] 'docker-compose' not found. Is Docker installed and in your PATH?")
            raise typer.Exit(code=1)

    def restore(self):
        """Restores the database from a backup file with interactive prompts."""
        self.console.print(f"\n[bold yellow]Initiating restore for '{self.env}' environment...[/bold yellow]")

        backup_file = self._select_backup_file()
        self.console.print(f"\nYou have selected to restore: [bold cyan]{backup_file.name}[/bold cyan]")
        
        warning = f"\n[bold red]WARNING:[/bold red] This will WIPE the '{self.env}' database and replace it."
        self.console.print(warning)
        if not Confirm.ask("Are you absolutely sure you want to continue?"):
            self.console.print("[yellow]Restore cancelled.[/yellow]")
            raise typer.Exit()

        self.console.print(f"\nRestoring from [cyan]{backup_file.name}[/cyan]...")
        
        restore_command = (
            f"docker-compose -f {self.compose_file} exec -T db "
            f"pg_restore -U {self.pg_user} -d {self.pg_db} --clean --if-exists"
        )

        try:
            with open(backup_file, "rb") as f_in:
                subprocess.run(
                    shlex.split(restore_command),
                    stdin=f_in,
                    check=True,
                    capture_output=True,
                    cwd=PROJECT_ROOT # Explicitly set the working directory to CaptainDock root
                )
            self.console.print("\n[bold green]Success![/bold green] Database restore complete.")
        except subprocess.CalledProcessError as e:
            self.console.print(f"[bold red]Error during pg_restore:[/bold red]")
            self.console.print(e.stderr.decode('utf-8'))
            raise typer.Exit(code=1)
        except FileNotFoundError:
            self.console.print(f"[bold red]Error:[/bold red] 'docker-compose' not found. Is Docker installed and in your PATH?")
            raise typer.Exit(code=1)

    def _select_backup_file(self) -> Path:
        """Prompts the user to select a backup file from the available list."""
        if not self.backups_dir.exists() or not any(self.backups_dir.iterdir()):
            self.console.print(f"[bold red]Error:[/bold red] No backup files found in '{self.backups_dir}'.")
            raise typer.Exit(code=1)

        self.console.print("Available backup files:")
        backups = sorted([f for f in self.backups_dir.glob(f"{self.env}-backup-*.dump")], reverse=True)
        
        if not backups:
            self.console.print(f"[bold red]Error:[/bold red] No backups found for the '{self.env}' environment.")
            raise typer.Exit(code=1)

        for i, file in enumerate(backups):
            self.console.print(f"  [cyan]{i+1}[/cyan]: {file.name}")
        
        choice = Prompt.ask(
            "\nEnter the number of the backup file to restore", 
            choices=[str(i+1) for i in range(len(backups))],
            default="1"
        )
        return backups[int(choice) - 1]

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

if __name__ == "__main__":
    app()

