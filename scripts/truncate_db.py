import sys
from pathlib import Path

# --- Add project root to Python path ---
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))
# ---

from dotenv import load_dotenv
from rich.console import Console
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import Base

console = Console()

def truncate_database():
    """
    Connects to the database and drops and recreates all tables.
    USE WITH CAUTION! This will permanently delete all data.
    """
    console.print("\n--- Database Truncate Utility ---", style="bold yellow")
    
    # Confirm the operation
    if '--yes' in sys.argv:
        confirm = 'yes'
    else:
        confirm = console.input(
            "[bold red]WARNING: This will permanently delete all data. Are you sure? (yes/no): [/bold red]"
        )
    if confirm.lower() != "yes":
        console.print("Operation cancelled.", style="green")
        return

    try:
        console.print(f"Connecting to database at {settings.DATABASE_URL}...", style="cyan")
        engine = create_engine(str(settings.DATABASE_URL))
        
        console.print("Dropping all tables...", style="yellow")
        Base.metadata.drop_all(bind=engine)
        
        console.print("Recreating all tables...", style="yellow")
        Base.metadata.create_all(bind=engine)
        
        console.print("\nDatabase has been successfully truncated.", style="bold green")

    except Exception as e:
        console.print(f"\nAn unexpected error occurred: {e}", style="bold red")

if __name__ == "__main__":
    # Load environment variables to ensure the database connection is available.
    # We set APP_ENV to 'local' to ensure it connects to localhost.
    import os
    os.environ['APP_ENV'] = 'local'
    env_path = root_dir.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    
    truncate_database()
