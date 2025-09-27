from sqlalchemy.orm import Session
import uuid
from typing import List, Optional

from app.core.exceptions import AppException
from fastapi import status
from app.models.user import User
from app.models.account_ledger import AccountLedger
from app.models.payment import Payment, PaymentDirection
from app.repository.account_ledger import account_ledger_repo
from app.schema.account_ledger import AccountLedgerCreate, AccountLedgerUpdate
from app.repository.contact import contact_repo


class AccountLedgerService:
    """Service layer for account ledger business logic."""

    def get_by_id(self, db: Session, *, account_ledger_id: uuid.UUID) -> AccountLedger:
        """Helper method to get a ledger entry by ID or raise 404."""
        ledger = account_ledger_repo.get(db, id=account_ledger_id)
        if not ledger:
            raise AppException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Account ledger with ID {account_ledger_id} not found.")
        return ledger

    def create(self, db: Session, *, ledger_in: AccountLedgerCreate, current_user: User) -> AccountLedger:
        """Handles business logic for creating a new ledger entry."""
        if not contact_repo.get(db, id=ledger_in.contact_id):
             raise AppException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with ID {ledger_in.contact_id} not found.")
        
        return account_ledger_repo.create(db, obj_in=ledger_in)

    def update(self, db: Session, *, ledger_id: uuid.UUID, ledger_in: AccountLedgerUpdate, current_user: User) -> AccountLedger:
        """Handles business logic for updating a ledger entry."""
        ledger = self.get_by_id(db, account_ledger_id=ledger_id)
        return account_ledger_repo.update(db, db_obj=ledger, obj_in=ledger_in)

    def delete(self, db: Session, *, ledger_id: uuid.UUID, current_user: User) -> AccountLedger:
        """Handles business logic for deleting a ledger entry."""
        return account_ledger_repo.remove(db, id=ledger_id)

    def update_debt_from_payment(self, db: Session, *, payment: Payment):
        """Updates the debt of the associated ledger based on an approved payment."""
        if not payment.account_ledger_id:
            return
        
        ledger = self.get_by_id(db, account_ledger_id=payment.account_ledger_id)
        if payment.direction == PaymentDirection.OUTGOING or payment.direction == PaymentDirection.INTERNAL_TRANSFER:
            ledger.debt -= payment.amount # Customer pays down their debt
        
        db.commit()
    
    def revert_debt_from_payment(self, db: Session, *, payment: Payment):
        """Reverts a debt change on the associated ledger when a payment is rejected."""
        if not payment.account_ledger_id:
            return
        
        ledger = self.get_by_id(db, account_ledger_id=payment.account_ledger_id)
        if payment.direction == PaymentDirection.OUTGOING or payment.direction == PaymentDirection.INTERNAL_TRANSFER:
            ledger.debt += payment.amount # Add back the debt
            
        db.commit()

account_ledger_service = AccountLedgerService()

