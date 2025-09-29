import sys
from pathlib import Path

# --- Add project root to Python path ---
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))
# ---

from dotenv import load_dotenv
from rich.console import Console
from sqlalchemy import create_engine, text

from app.core.config import settings

console = Console()

def truncate_audit_log_table():
    """
    Connects to the database and truncates ONLY the audit_log table.
    """
    console.print("\n--- Audit Log Truncate Utility ---", style="bold yellow")
    
    if '--yes' in sys.argv:
        confirm = 'yes'
    else:
        confirm = console.input(
            "[bold red]WARNING: This will permanently delete all audit log data. Are you sure? (yes/no): [/bold red]"
        )
        
    if confirm.lower() != "yes":
        console.print("Operation cancelled.", style="green")
        return

    try:
        engine = create_engine(str(settings.DATABASE_URL))
        with engine.connect() as connection:
            with connection.begin():
                console.print("Truncating audit_log table...", style="yellow")
                connection.execute(text('TRUNCATE TABLE audit_log RESTART IDENTITY;'))
        
        console.print("\nAudit log table has been successfully truncated.", style="bold green")

    except Exception as e:
        console.print(f"\nAn unexpected error occurred: {e}", style="bold red")

if __name__ == "__main__":
    import os
    os.environ['APP_ENV'] = 'local'
    env_path = root_dir.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    
    truncate_audit_log_table()
