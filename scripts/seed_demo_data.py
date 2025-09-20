import sys
from pathlib import Path

# --- Add project root to Python path ---
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))
# ---

from dotenv import load_dotenv
from rich.console import Console
from app.db.session import SessionLocal
from app.services.user import user_service
from app.services.contact import contact_service
from app.services.saved_bank_account import saved_bank_account_service
from app.repository.user import user_repo
from app.repository.saved_bank_account import saved_bank_account_repo
from seeding.data.demo_data import DEMO_USERS, DEMO_CONTACTS, DEMO_SAVED_BANK_ACCOUNTS
from app.models.user import User

console = Console()

def seed_demo_data():
    """
    Populates the database with a set of demo data.
    Checks for existence before creating to avoid duplicates.
    """
    console.print("\n--- Seeding Demo Data ---", style="bold")
    db = SessionLocal()
    try:
        # --- Seed Users ---
        console.print("\nSeeding demo users...", style="yellow")
        for user_in in DEMO_USERS:
            user = user_repo.get_by_username(db, username=user_in.username)
            if user:
                console.print(f"User '[cyan]{user_in.username}[/cyan]' already exists. Skipping.", style="dim")
            else:
                user_service.create_user(db, user_in=user_in)
                console.print(f"Created user: '[bold green]{user_in.username}[/bold green]'", style="green")

        # --- Seed Contacts ---
        console.print("\nSeeding demo contacts...", style="yellow")
        for contact_data in DEMO_CONTACTS:
            owner_username = contact_data["owner_username"]
            contact_in = contact_data["contact"]
            
            owner = user_repo.get_by_username(db, username=owner_username)
            if not owner:
                console.print(f"Owner user '[cyan]{owner_username}[/cyan]' not found for contact. Skipping.", style="dim red")
                continue

            if contact_in.phone_number:
                 existing_contact = db.query(Contact).filter(Contact.phone_number == contact_in.phone_number).first()
                 if existing_contact:
                      console.print(f"Contact for '[cyan]{contact_in.first_name} {contact_in.last_name}[/cyan]' with this phone number already exists. Skipping.", style="dim")
                      continue

            contact_service.create_contact(db, contact_in=contact_in, current_user=owner)
            console.print(f"Created contact: '[bold green]{contact_in.first_name} {contact_in.last_name}[/bold green]' for user '[cyan]{owner_username}[/cyan]'", style="green")
        
        admin_user = user_repo.get_by_username(db=db, username='admin')
        console.print("\nSeeding demo saved bank accounts...", style="yellow")
        for account_in in DEMO_SAVED_BANK_ACCOUNTS:
            account = saved_bank_account_repo.get_by_name(db, name=account_in.name)
            if account:
                console.print(f"Bank Account '[cyan]{account_in.name}[/cyan]' already exists. Skipping.", style="dim")
            else:
                saved_bank_account_service.create(db, account_in=account_in)
                console.print(f"Created bank account: '[bold green]{account_in.name}[/bold green]'", style="green")


        console.print("\n✅ Demo data seeding complete!", style="bold green")

    except Exception as e:
        console.print(f"\nAn unexpected error occurred: {e}", style="bold red")
    finally:
        db.close()

if __name__ == "__main__":
    from app.models.contact import Contact # Local import to avoid circular dependency issues
    env_path = root_dir.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    
    seed_demo_data()

