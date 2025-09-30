"""
Handles all configuration, path resolution, and environment variable loading.
This module acts as a single source of truth for all script settings.
"""

import os
import sys
from pathlib import Path

import typer
from dotenv import load_dotenv
from rich.console import Console

# --- Path Setup ---
# Assumes this module is part of a script run from the 'backend' directory.
BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = BACKEND_ROOT.parent

# Add backend root to Python path to allow app-level imports if needed.
sys.path.insert(0, str(BACKEND_ROOT))


class AppConfig:
    """Singleton class to hold all application configuration for the script."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance._load_env()
            
            cls.CONSOLE = Console()
            cls.PROJECT_ROOT = PROJECT_ROOT
            cls.BACKUPS_DIR = PROJECT_ROOT / "backups"
            cls.PG_USER = os.getenv("POSTGRES_USER")
            cls.PG_DB = os.getenv("POSTGRES_DB")

            if not all([cls.PG_USER, cls.PG_DB]):
                cls.CONSOLE.print("[bold red]Error:[/bold red] Required env vars (POSTGRES_USER, POSTGRES_DB) not set.")
                raise typer.Exit(code=1)
        return cls._instance

    def _load_env(self):
        """Finds and loads the .env file from the project root."""
        env_path = PROJECT_ROOT / ".env"
        if not env_path.exists():
            # Use a temporary console for this initial error, as the main one isn't set yet.
            Console().print(f"[bold red]Error:[/bold red] '.env' file not found at '{env_path}'.")
            raise typer.Exit(code=1)
        load_dotenv(dotenv_path=env_path)

    def get_compose_file(self, env: str) -> str:
        """Gets the correct docker-compose filename for the given environment."""
        compose_files = {
            "dev": "docker-compose.dev.yml",
            "prod": "docker-compose.prod.yml",
        }
        file_name = compose_files.get(env)
        if not file_name:
            self.CONSOLE.print(f"[bold red]Error:[/bold red] Invalid environment '{env}'. Choose 'dev' or 'prod'.")
            raise typer.Exit(code=1)
        return file_name

# Create a single, importable instance of the configuration.
config = AppConfig()
