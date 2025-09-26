import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import status

from app.core.exceptions import AppException
from app.models.user import User
from app.models.account_ledger import AccountLedger
from app.repository.account_ledger import account_ledger_repo
from app.schema.account_ledger import AccountLedgerCreate, AccountLedgerUpdate
from app.services.contact import contact_service
from app.services.transaction import transaction_service

class AccountLedgerService:
    """Service layer for account ledger business logic."""

    def get_by_id(self, db: Session, *, ledger_id: uuid.UUID) -> AccountLedger:
        """Get a single account ledger entry by its ID."""
        ledger = account_ledger_repo.get(db, id=ledger_id)
        if not ledger:
            raise AppException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Account ledger with ID {ledger_id} not found.")
        return ledger

    def search(self, db: Session, **kwargs) -> List[AccountLedger]:
        """Search for account ledger entries."""
        return account_ledger_repo.search(db, **kwargs)

    def create(self, db: Session, *, ledger_in: AccountLedgerCreate, current_user: User) -> AccountLedger:
        """Create a new account ledger entry."""
        # Validate that the contact exists
        contact_service.get_contact_by_id(db, contact_id=ledger_in.contact_id)

        # Validate transaction exists if provided
        if ledger_in.transaction_id:
            # Note: We pass the current_user here to satisfy the permission check in the transaction service,
            # even though ledger access itself is not restricted by user.
            transaction_service.get_transaction_by_id(db, transaction_id=ledger_in.transaction_id, current_user=current_user)
            
        return account_ledger_repo.create(db, obj_in=ledger_in)

    def update(self, db: Session, *, ledger_id: uuid.UUID, ledger_in: AccountLedgerUpdate) -> AccountLedger:
        """Update an account ledger entry."""
        ledger_to_update = self.get_by_id(db, ledger_id=ledger_id)
        return account_ledger_repo.update(db, db_obj=ledger_to_update, obj_in=ledger_in)

    def delete(self, db: Session, *, ledger_id: uuid.UUID) -> AccountLedger:
        """Delete an account ledger entry."""
        self.get_by_id(db, ledger_id=ledger_id)
        return account_ledger_repo.remove(db, id=ledger_id)

account_ledger_service = AccountLedgerService()

