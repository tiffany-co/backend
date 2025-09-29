import sys
from pathlib import Path

# --- Add project root to Python path ---
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))
# ---

from dotenv import load_dotenv
from rich.console import Console
from sqlalchemy.orm import Session
import traceback

# --- Repositories ---
from app.repository.user import user_repo
from app.repository.contact import contact_repo
from app.repository.saved_bank_account import saved_bank_account_repo
from app.repository.inventory import inventory_repo

# --- Services ---
from app.services.user import user_service
from app.services.contact import contact_service
from app.services.saved_bank_account import saved_bank_account_service
from app.services.inventory import inventory_service

# --- Demo Data & Runner ---
from seeding.data.demo_data import (
    DEMO_USERS,
    DEMO_CONTACTS,
    DEMO_SAVED_BANK_ACCOUNTS,
    DEMO_INVENTORY,
    DEMO_SCENARIOS
)
from seeding.scenario_runner import ScenarioRunner
from app.db.session import SessionLocal

console = Console()

def seed_demo_data():
    """
    Populates the database with a comprehensive and interconnected set of demo data.
    Checks for existence before creating to avoid duplicates on re-runs.
    """
    console.print("\n--- Seeding Demo Data ---", style="bold")
    db = SessionLocal()
    try:
        # --- 1. Basic Setup ---
        _seed_users(db)
        _seed_contacts(db)
        _seed_saved_bank_accounts(db)
        _seed_initial_inventory(db)

        # --- 2. Complex Scenarios ---
        for scenario_data in DEMO_SCENARIOS:
            runner = ScenarioRunner(db, scenario_data)
            runner.run()

        console.print("\nDemo data seeding complete!", style="bold green")

    except Exception as e:
        console.print(f"\nAn unexpected error occurred: {e}", style="bold red")
        console.print(traceback.format_exc())
    finally:
        db.close()


def _seed_users(db: Session):
    console.print("\n[1/5] Seeding demo users...", style="yellow")
    for user_in in DEMO_USERS:
        if not user_repo.get_by_username(db, username=user_in.username):
            user_service.create_user(db, user_in=user_in)
            console.print(f"   - Created user: '[bold green]{user_in.username}[/bold green]'")
        else:
            console.print(f"   - User '[cyan]{user_in.username}[/cyan]' already exists. Skipping.")

def _seed_contacts(db: Session):
    console.print("\n[2/5] Seeding demo contacts...", style="yellow")
    for contact_data in DEMO_CONTACTS:
        owner = user_repo.get_by_username(db, username=contact_data["owner_username"])
        contact_in = contact_data["contact"]
        if not contact_repo.get_by_national_number(db, national_number=contact_in.national_number):
            contact_service.create_contact(db, contact_in=contact_in, current_user=owner)
            console.print(f"   - Created contact: '[bold green]{contact_in.first_name} {contact_in.last_name}[/bold green]'")
        else:
            console.print(f"   - Contact for '[cyan]{contact_in.first_name} {contact_in.last_name}[/cyan]' already exists. Skipping.")

def _seed_saved_bank_accounts(db: Session):
    console.print("\n[3/5] Seeding demo saved bank accounts...", style="yellow")
    for account_in in DEMO_SAVED_BANK_ACCOUNTS:
        if not saved_bank_account_repo.get_by_name(db, name=account_in.name):
            saved_bank_account_service.create(db, account_in=account_in)
            console.print(f"   - Created bank account: '[bold green]{account_in.name}[/bold green]'")
        else:
            console.print(f"   - Bank Account '[cyan]{account_in.name}[/cyan]' already exists. Skipping.")

def _seed_initial_inventory(db: Session):
    console.print("\n[4/5] Seeding initial inventory...", style="yellow")
    if not inventory_repo.get_latest(db):
        inventory_service.adjust_inventory(db, adjustment_in=DEMO_INVENTORY)
        console.print("   - Created initial inventory snapshot.", style="green")
    else:
        console.print("   - Inventory already has records. Skipping initial snapshot.", style="dim")


if __name__ == "__main__":
    env_path = root_dir.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    
    seed_demo_data()

