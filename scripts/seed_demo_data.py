import sys
from pathlib import Path

# --- Add project root to Python path ---
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))
# ---

from dotenv import load_dotenv
from rich.console import Console
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
import traceback

# --- Models & Enums ---
from app.models.enums.shared import ApprovalStatus

# --- Repositories ---
from app.repository.user import user_repo
from app.repository.contact import contact_repo
from app.repository.saved_bank_account import saved_bank_account_repo
from app.repository.inventory import inventory_repo
from app.repository.transaction import transaction_repo
from app.repository.account_ledger import account_ledger_repo
from app.repository.payment import payment_repo
from app.repository.item import item_repo

# --- Services ---
from app.services.user import user_service
from app.services.contact import contact_service
from app.services.saved_bank_account import saved_bank_account_service
from app.services.inventory import inventory_service
from app.services.transaction import transaction_service
from app.services.transaction_item import transaction_item_service
from app.services.account_ledger import account_ledger_service
from app.services.payment import payment_service

# --- Demo Data ---
from seeding.data.demo_data import (
    DEMO_USERS,
    DEMO_CONTACTS,
    DEMO_SAVED_BANK_ACCOUNTS,
    DEMO_INVENTORY,
    TRANSACTION_1_BUY_GOLD,
    TRANSACTION_2_SELL_GOLD,
    TRANSACTION_3_BUY_MORE_GOLD
)
from app.schema.transaction import TransactionCreate
from app.schema.transaction_item import TransactionItemCreate
from app.schema.account_ledger import AccountLedgerCreate
from app.schema.payment import PaymentCreate

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
        _run_transaction_1(db)
        _run_transaction_2(db)
        # _run_transaction_3(db)

        console.print("\nDemo data seeding complete!", style="bold green")

    except Exception as e:
        console.print(f"\nAn unexpected error occurred: {e}", style="bold red")
        console.print(traceback.format_exc())
    finally:
        db.close()


def _seed_users(db: Session):
    console.print("\n[1/7] Seeding demo users...", style="yellow")
    for user_in in DEMO_USERS:
        if not user_repo.get_by_username(db, username=user_in.username):
            user_service.create_user(db, user_in=user_in)
            console.print(f"  - Created user: '[bold green]{user_in.username}[/bold green]'")
        else:
            console.print(f"  - User '[cyan]{user_in.username}[/cyan]' already exists. Skipping.")

def _seed_contacts(db: Session):
    console.print("\n[2/7] Seeding demo contacts...", style="yellow")
    for contact_data in DEMO_CONTACTS:
        owner = user_repo.get_by_username(db, username=contact_data["owner_username"])
        contact_in = contact_data["contact"]
        if not contact_repo.get_by_national_number(db, national_number=contact_in.national_number):
            contact_service.create_contact(db, contact_in=contact_in, current_user=owner)
            console.print(f"  - Created contact: '[bold green]{contact_in.first_name} {contact_in.last_name}[/bold green]'")
        else:
            console.print(f"  - Contact for '[cyan]{contact_in.first_name} {contact_in.last_name}[/cyan]' already exists. Skipping.")

def _seed_saved_bank_accounts(db: Session):
    console.print("\n[3/7] Seeding demo saved bank accounts...", style="yellow")
    for account_in in DEMO_SAVED_BANK_ACCOUNTS:
        if not saved_bank_account_repo.get_by_name(db, name=account_in.name):
            saved_bank_account_service.create(db, account_in=account_in)
            console.print(f"  - Created bank account: '[bold green]{account_in.name}[/bold green]'")
        else:
            console.print(f"  - Bank Account '[cyan]{account_in.name}[/cyan]' already exists. Skipping.")

def _seed_initial_inventory(db: Session):
    console.print("\n[4/7] Seeding initial inventory...", style="yellow")
    if not inventory_repo.get_latest(db):
        inventory_service.adjust_inventory(db, adjustment_in=DEMO_INVENTORY)
        console.print("  - Created initial inventory snapshot.", style="green")
    else:
        console.print("  - Inventory already has records. Skipping initial snapshot.", style="dim")


def _run_transaction_1(db: Session):
    console.print("\n[5/7] Running Transaction Scenario 1 (Buy Gold & Create Debt)...", style="yellow")
    
    # --- Dependencies ---
    recorder = user_repo.get_by_username(db, username=TRANSACTION_1_BUY_GOLD["recorder_username"])
    contact = contact_repo.get_by_national_number(db, national_number=TRANSACTION_1_BUY_GOLD["contact_national_number"])
    
    # --- Check if transaction already exists ---
    if transaction_repo.get_by_note(db, note=TRANSACTION_1_BUY_GOLD["transaction"]["note"]):
        console.print("  - Transaction 1 already exists. Skipping scenario.", style="dim")
        return

    # --- Create Transaction and Items ---
    trans_create = TRANSACTION_1_BUY_GOLD["transaction"]
    trans_create['contact_id'] = contact.id
    trans_create_schema = TransactionCreate(**trans_create)
    new_transaction = transaction_service.create(db, transaction_in=trans_create_schema, current_user=recorder)

    for item_data in TRANSACTION_1_BUY_GOLD["items"]:
        item_model = item_repo.get_by_name(db, name=item_data["item_name"])
        del item_data['item_name']
        item_data['transaction_id'] = new_transaction.id
        item_data['item_id'] = item_model.id
        item_create_schema = TransactionItemCreate(**item_data)
        transaction_item_service.create_item(db, item_in=item_create_schema, current_user=recorder)
    
    # --- Approve Transaction ---
    admin_user = user_repo.get_by_username(db, username='admin')
    transaction_service.approve(db, transaction_id=new_transaction.id, current_user=recorder)
    transaction_service.approve(db, transaction_id=new_transaction.id, current_user=admin_user)
    
    # --- Create Ledger Entry ---
    db.refresh(new_transaction) # Refresh to get the calculated total_price
    ledger_create = TRANSACTION_1_BUY_GOLD["ledger"]
    ledger_create['contact_id'] = contact.id
    ledger_create['transaction_id'] = new_transaction.id
    ledger_create['debt'] = abs(new_transaction.total_price) # Debt is the total cost we owe
    ledger_create_schema = AccountLedgerCreate(**ledger_create)
    account_ledger_service.create(db, ledger_in=ledger_create_schema)
    
    console.print(f"  - Scenario 1 complete for contact: '[bold green]{contact.last_name}[/bold green]'", style="green")


def _run_transaction_2(db: Session):
    console.print("\n[6/7] Running Transaction Scenario 2 (Sell Gold & Settle Debt)...", style="yellow")
    
    # --- Dependencies ---
    recorder = user_repo.get_by_username(db, username=TRANSACTION_2_SELL_GOLD["recorder_username"])
    contact_rezai = contact_repo.get_by_national_number(db, national_number=TRANSACTION_2_SELL_GOLD["contact_national_number"])
    contact_ahmadi = contact_repo.get_by_national_number(db, national_number=TRANSACTION_2_SELL_GOLD["payments"][0]["contact_national_number"])
    ledger_search_result = account_ledger_repo.search(db, contact_id=contact_ahmadi.id)
    ledger_ahmadi = ledger_search_result[0] if 1 <= len(ledger_search_result) else None
    bank_account = saved_bank_account_repo.get_by_name(db, name=TRANSACTION_2_SELL_GOLD["payments"][1]["saved_bank_account_name"])

    # --- Check if transaction already exists ---
    if transaction_repo.get_by_note(db, note=TRANSACTION_2_SELL_GOLD["transaction"]['note']):
        console.print("  - Transaction 2 already exists. Skipping scenario.", style="dim")
        return

    # --- Create Transaction and Items ---
    trans_create = TRANSACTION_2_SELL_GOLD["transaction"]
    trans_create['contact_id'] = contact_rezai.id
    trans_create_schema = TransactionCreate(**trans_create)
    new_transaction = transaction_service.create(db, transaction_in=trans_create_schema, current_user=recorder)

    for item_data in TRANSACTION_2_SELL_GOLD["items"]:
        item_model = item_repo.get_by_name(db, name=item_data["item_name"])
        del item_data['item_name']
        item_data['item_id'] = item_model.id
        item_data['transaction_id'] = new_transaction.id
        item_create_schema = TransactionItemCreate(**item_data)
        transaction_item_service.create_item(db, item_in=item_create_schema, current_user=recorder)

    # --- Approve Transaction by Admin ---
    transaction_service.approve(db, transaction_id=new_transaction.id, current_user=recorder)

    # --- Create and Approve Payments ---
    db.refresh(ledger_ahmadi)
    db.refresh(new_transaction)
    payment_internal_create = TRANSACTION_2_SELL_GOLD["payments"][0]
    payment_internal_create["amount"] = abs(new_transaction.total_price)
    payment_internal_create["account_ledger_id"] = ledger_ahmadi.id
    payment_internal_create.pop("contact_national_number") # Clean up temp field
    Payment_create_schema = PaymentCreate(**payment_internal_create)
    payment_internal = payment_service.create(db, payment_in=Payment_create_schema, current_user=recorder)
    payment_service.approve(db, payment_id=payment_internal.id, current_user=recorder)

    db.refresh(new_transaction) # Get final price
    remaining_payment = ledger_ahmadi.debt - payment_internal.amount
    
    payment_outgoing_create = TRANSACTION_2_SELL_GOLD["payments"][1]
    payment_outgoing_create["amount"] = remaining_payment
    payment_outgoing_create["contact_id"] = contact_rezai.id
    payment_outgoing_create["transaction_id"] = new_transaction.id
    payment_outgoing_create["saved_bank_account_id"] = bank_account.id
    payment_outgoing_create['account_ledger_id'] = ledger_ahmadi.id
    payment_outgoing_create['contact_id'] = ledger_ahmadi.contact_id
    payment_outgoing_create.pop("saved_bank_account_name")
    payment_outgoing_schema = PaymentCreate(**payment_outgoing_create)
    payment_outgoing = payment_service.create(db, payment_in=payment_outgoing_schema, current_user=recorder)
    payment_service.approve(db, payment_id=payment_outgoing.id, current_user=recorder)
    
    console.print(f"  - Scenario 2 complete for contact: '[bold green]{contact_rezai.last_name}[/bold green]'", style="green")


def _run_transaction_3(db: Session):
    console.print("\n[7/7] Running Transaction Scenario 3 (Buy Gold with Partial Payment)...", style="yellow")
    
    # --- Dependencies ---
    recorder = user_repo.get_by_username(db, username=TRANSACTION_3_BUY_MORE_GOLD["recorder_username"])
    contact = contact_repo.get_by_national_number(db, nationalget_by_national_number=TRANSACTION_3_BUY_MORE_GOLD["contact_nationalget_by_national_number"])

    # --- Check if transaction already exists ---
    if transaction_repo.get_by_note(db, note=TRANSACTION_3_BUY_MORE_GOLD["transaction"].note):
        console.print("  - Transaction 3 already exists. Skipping scenario.", style="dim")
        return
        
    # --- Create Transaction and Items ---
    trans_create = TRANSACTION_3_BUY_MORE_GOLD["transaction"]
    trans_create.contact_id = contact.id
    new_transaction = transaction_service.create(db, transaction_in=trans_create, current_user=recorder)

    for item_data in TRANSACTION_3_BUY_MORE_GOLD["items"]:
        item_model = item_repo.get_by_name(db, name=item_data["item_name"])
        item_create_schema = TransactionItemCreate(**item_data)
        transaction_item_service.create(db, transaction_id=new_transaction.id, item_in=item_create_schema, current_user=recorder, item_model=item_model)

    # --- Approve Transaction ---
    admin_user = user_repo.get_by_username(db, username='admin')
    transaction_service.approve(db, transaction_id=new_transaction.id, current_user=recorder)
    transaction_service.approve(db, transaction_id=new_transaction.id, current_user=admin_user)

    # --- Create and Approve Payment ---
    payment_create = TRANSACTION_3_BUY_MORE_GOLD["payment"]["payment"]
    payment_create["contact_id"] = contact.id
    payment_create["transaction_id"] = new_transaction.id
    payment_partial = payment_service.create(db, payment_in=payment_create, current_user=recorder)
    payment_service.approve(db, payment_id=payment_partial.id, current_user=admin_user)
    
    # --- Create Ledger for Remaining Debt ---
    db.refresh(new_transaction)
    remaining_debt = new_transaction.total_price + payment_partial.amount # total_price is negative
    
    ledger_create = TRANSACTION_3_BUY_MORE_GOLD["ledger"]
    ledger_create.contact_id = contact.id
    ledger_create.transaction_id = new_transaction.id
    ledger_create.debt = remaining_debt
    account_ledger_service.create(db, ledger_in=ledger_create, current_user=recorder)
    
    console.print(f"  - Scenario 3 complete for contact: '[bold green]{contact.last_name}[/bold green]'", style="green")


if __name__ == "__main__":
    env_path = root_dir.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    
    seed_demo_data()

