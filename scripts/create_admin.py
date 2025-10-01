import sys
from pathlib import Path
from getpass import getpass

# --- Add project root to Python path ---
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))
# ---

from dotenv import load_dotenv
from rich.console import Console
from fastapi import HTTPException
from app.db.session import SessionLocal
from app.schema.user import AdminCreate
from app.services.user import user_service
from app.models.enums.user import UserRole
from app.core.exceptions import AppException

# Initialize rich console for beautiful output
console = Console()

def create_admin():
    """
    Creates an admin user through an interactive and user-friendly command-line interface.
    """
    console.print("\n--- Create Admin User ---\n", style="bold")
    
    try:
        # --- Get user input ---
        console.print("Please provide the following details for the new admin user:", style="yellow")
        username = console.input("[bold]Enter username:[/bold] ")
        full_name = console.input("[bold]Enter your full name:[/bold] ").strip() or None
        phone_number = console.input("[bold]Enter phone number:[/bold] ").strip() or None
        
        # --- Get password securely ---
        password = getpass("Enter password (input will be hidden): ")
        if not password:
            console.print("\nPassword cannot be empty. Aborting.", style="bold red")
            return
            
        confirm_password = getpass("Confirm password: ")

        if password != confirm_password:
            console.print("\nPasswords do not match. Aborting.", style="bold red")
            return

        # --- Create user in database ---
        db = SessionLocal()

        # Use the AdminCreate schema which includes the 'role' field
        admin_data = AdminCreate(
            username=username,
            full_name=full_name,
            phone_number=phone_number,
            password=password,
            role=UserRole.ADMIN,
            is_active=True,
        )

        user = user_service.create_user(db=db, user_in=admin_data)
        
        console.print(f"\nAdmin user '[bold cyan]{user.username}[/bold cyan]' created successfully!", style="green")

    except HTTPException as e:
        # Catch the specific error from the service layer and display its detail
        console.print(f"\nError: {e.detail}", style="bold red")
    except AppException as e:
        console.print(f"\nError: {e.detail}", style="bold red")
    except Exception as e:
        # Catch any other unexpected errors
        console.print(f"\nAn unexpected error occurred: {e}", style="bold red")
    finally:
        if 'db' in locals() and db:
            db.close()

if __name__ == "__main__":
    # Load environment variables from the root .env file
    env_path = root_dir.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    
    create_admin()

