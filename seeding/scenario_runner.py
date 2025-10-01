from sqlalchemy.orm import Session
from rich.console import Console
from typing import Dict, Any

# --- Schemas ---
from app.schema.transaction import TransactionCreate
from app.schema.transaction_item import TransactionItemCreate
from app.schema.account_ledger import AccountLedgerCreate
from app.schema.payment import PaymentCreate

# --- Repositories ---
from app.repository.user import user_repo
from app.repository.contact import contact_repo
from app.repository.item import item_repo
from app.repository.transaction import transaction_repo
from app.repository.account_ledger import account_ledger_repo
from app.repository.saved_bank_account import saved_bank_account_repo
from app.repository.investor import investor_repo
from app.repository.payment import payment_repo

# --- Services ---
from app.services.transaction import transaction_service
from app.services.transaction_item import transaction_item_service
from app.services.account_ledger import account_ledger_service
from app.services.payment import payment_service

console = Console()

class ScenarioRunner:
    """
    Handles the logic for executing a single, complex demo data scenario.
    This class encapsulates data fetching, object creation, and state management,
    keeping the main seeder script clean and readable.
    """
    def __init__(self, db: Session, scenario_data: Dict[str, Any]):
        self.db = db
        self.data = scenario_data
        self.dependencies = {}
        self.created_objects = {}

    def run(self):
        """Public method to execute the scenario."""
        console.print(f"\n[6/6] Running '[bold blue]{self.data['name']}[/bold blue]'...", style="yellow")
        
        # Check if the scenario has already been run to ensure idempotency.
        ignore = False
        if "transaction" in self.data:
            # For transaction-based scenarios, check by the unique transaction note.
            if transaction_repo.get_by_note(self.db, note=self.data["transaction"]["note"]):
                ignore = True
        # For payment-only scenarios, check by the description of the first payment.
        elif "payments" in self.data:
            first_payment_description = self.data["payments"][0].get("description")
            if first_payment_description and payment_repo.get_by_description(self.db, description=first_payment_description):
                ignore = True
                
        if ignore:
            console.print(f"   - Scenario already run. Skipping.", style="dim")
            return
        
        self._fetch_dependencies()
        
        if "transaction" in self.data:
            self._create_transaction_and_items()
            self._approve_transaction()
            self._process_ledger()

        self._process_payments()


        console.print(f"   - Scenario '{self.data['name']}' complete.", style="green")

    def _fetch_dependencies(self):
        """Fetches all required existing objects from the DB."""
        self.dependencies['recorder'] = user_repo.get_by_username(self.db, username=self.data["recorder_username"])
        self.dependencies['admin'] = user_repo.get_by_username(self.db, username='admin')
        
        if self.data.get("contact_national_number"):
            self.dependencies['contact'] = contact_repo.get_by_national_number(self.db, national_number=self.data["contact_national_number"])
        
        if self.data.get("investor_username"):
            self.dependencies['investor'] = investor_repo.get_by_username(self.db, username=self.data["investor_username"])

    def _create_transaction_and_items(self):
        """Creates the main transaction and its associated items."""
        trans_data = self.data["transaction"].copy()
        trans_data['contact_id'] = self.dependencies['contact'].id
        trans_schema = TransactionCreate(**trans_data)
        transaction = transaction_service.create(self.db, transaction_in=trans_schema, current_user=self.dependencies['recorder'])
        
        for item_data in self.data.get("items", []):
            item_model = item_repo.get_by_name(self.db, name=item_data["item_name"])
            
            item_create_data = item_data.copy()
            item_create_data.pop("item_name")
            item_create_data['item_id'] = item_model.id
            item_create_data['transaction_id'] = transaction.id
            
            item_schema = TransactionItemCreate(**item_create_data)
            transaction_item_service.create_item(self.db, item_in=item_schema, current_user=self.dependencies['recorder'])
        
        self.created_objects['transaction'] = transaction

    def _approve_transaction(self):
        """Approves the transaction by both user and admin."""
        transaction = self.created_objects['transaction']
        transaction_service.approve(self.db, transaction_id=transaction.id, current_user=self.dependencies['recorder'])
        if not self._is_recorder_admin():
            transaction_service.approve(self.db, transaction_id=transaction.id, current_user=self.dependencies['admin'])
        self.db.refresh(transaction) # Refresh to get final total_price

    def _is_recorder_admin(self):
        return self.dependencies['recorder'] == self.dependencies['admin']

    def _process_payments(self):
        """Handles the creation and approval of single or multiple payments."""
        payments_data = self.data.get("payments") or []

        for payment_data in payments_data:
            self._create_and_approve_payment(payment_data)

    def _create_and_approve_payment(self, payment_data: Dict[str, Any]):
        """Creates and approves a single payment."""
        recorder = self.dependencies['recorder']
        transaction = self.created_objects.get('transaction')
        investor = self.dependencies.get('investor')
        
        payment_create_data = payment_data.copy()
        if transaction:
            payment_create_data.setdefault('transaction_id', transaction.id)
            payment_create_data.setdefault('contact_id', self.dependencies['contact'].id)
        if investor:
            payment_create_data.setdefault('investor_id', investor.id)

        # Handle dynamic amount calculation for debt settlement
        if payment_data.get("amount_description"):
            self._calculate_payment_amount(payment_create_data)

        # Link to saved bank account if specified
        if "saved_bank_account_name" in payment_create_data:
            bank = saved_bank_account_repo.get_by_name(self.db, name=payment_create_data["saved_bank_account_name"])
            payment_create_data["saved_bank_account_id"] = bank.id
            payment_create_data.pop("saved_bank_account_name")

        payment_schema = PaymentCreate(**payment_create_data)
        payment = payment_service.create(self.db, payment_in=payment_schema, current_user=recorder)
        payment_service.approve(self.db, payment_id=payment.id, current_user=recorder)
        if not self._is_recorder_admin():
            payment_service.approve(self.db, payment_id=payment.id, current_user=self.dependencies['admin'])
        
        self.created_objects['last_payment'] = payment

    def _calculate_payment_amount(self, payment_create_data: Dict[str, Any]):
        """Calculates payment amounts for complex settlement scenarios."""
        settle_contact = contact_repo.get_by_national_number(self.db, national_number=payment_create_data["settle_contact_national_number"])
        ledger = account_ledger_repo.search(self.db, contact_id=settle_contact.id)[0]
        payment_create_data['account_ledger_id'] = ledger.id
        
        if payment_create_data["amount_description"] == "SETTLE_PREVIOUS_DEBT":
            payment_create_data["amount"] = min(ledger.debt, abs(self.created_objects['transaction'].total_price))
        elif payment_create_data["amount_description"] == "REMAINDER_OF_PREVIOUS_DEBT":
            self.db.refresh(ledger)
            payment_create_data["amount"] = ledger.debt

        payment_create_data.pop("settle_contact_national_number")
        payment_create_data.pop("amount_description")


    def _process_ledger(self):
        """Creates a ledger entry if specified in the scenario."""
        if "ledger" not in self.data:
            return

        transaction = self.created_objects['transaction']
        
        ledger_data = self.data["ledger"].copy()
        ledger_data['contact_id'] = self.dependencies['contact'].id
        ledger_data['transaction_id'] = transaction.id

        # Calculate debt based on transaction total and payments made
        total_cost = abs(transaction.total_price)
        paid_amount = (self.created_objects.get('last_payment').amount if 'last_payment' in self.created_objects else 0)
        ledger_data['debt'] = total_cost - paid_amount
        
        if ledger_data['debt'] > 0:
            ledger_schema = AccountLedgerCreate(**ledger_data)
            account_ledger_service.create(self.db, ledger_in=ledger_schema)
