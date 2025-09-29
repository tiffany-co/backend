import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import status

from app.core.exceptions import AppException
from app.models.user import User, UserRole
from app.models.transaction import Transaction
from app.models.enums.transaction import TransactionType
from app.models.enums.shared import ApprovalStatus
from app.repository.transaction import transaction_repo
from app.schema.transaction import TransactionCreate, TransactionUpdate
from app.services.inventory import inventory_service
from app.services.contact import contact_service # Import contact service for validation

class TransactionService:
    """Service layer for transaction business logic."""

    def get_by_id(self, db: Session, *, transaction_id: uuid.UUID, current_user: User, with_items: bool = False) -> Transaction:
        if with_items:
            transaction = transaction_repo.get_with_items(db, id=transaction_id)
        else:
            transaction = transaction_repo.get(db, id=transaction_id)

        if not transaction:
            raise AppException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction with ID {transaction_id} not found.")
        
        if current_user.role != UserRole.ADMIN and transaction.recorder_id != current_user.id:
            raise AppException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to view this transaction.")
            
        return transaction

    def search(self, db: Session, *, current_user: User, **kwargs) -> List[Transaction]:
        return transaction_repo.search(db, current_user=current_user, **kwargs)

    def create(self, db: Session, *, transaction_in: TransactionCreate, current_user: User) -> Transaction:
        # Validate that the contact exists before creating the transaction
        contact_service.get_contact_by_id(db, contact_id=transaction_in.contact_id)
        
        create_data = transaction_in.model_dump()
        create_data["recorder_id"] = current_user.id
        return transaction_repo.create(db, obj_in=create_data)

    def update(self, db: Session, *, transaction_id: uuid.UUID, transaction_in: TransactionUpdate, current_user: User) -> Transaction:
        transaction = self.get_by_id(db, transaction_id=transaction_id, current_user=current_user)
        if transaction.status != ApprovalStatus.DRAFT:
            raise AppException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only transactions in 'draft' status can be updated.")
        
        # If contact_id is being updated, validate it exists
        if transaction_in.contact_id:
            contact_service.get_contact_by_id(db, contact_id=transaction_in.contact_id)

        updated_transaction = transaction_repo.update(db, db_obj=transaction, obj_in=transaction_in)
        self._recalculate_total_price(db, transaction=updated_transaction)
        return updated_transaction


    def delete(self, db: Session, *, transaction_id: uuid.UUID, current_user: User) -> Transaction:
        transaction = self.get_by_id(db, transaction_id=transaction_id, current_user=current_user)
        if transaction.status != ApprovalStatus.DRAFT:
            raise AppException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only transactions in 'draft' status can be deleted.")
        
        # Before deleting, nullify the link from any inventory entries
        db.refresh(transaction, attribute_names=['inventory_entries'])
        for entry in transaction.inventory_entries:
            entry.transaction_id = None
            db.add(entry)
        
        return transaction_repo.remove(db, id=transaction.id)

    def _recalculate_total_price(self, db: Session, transaction: Transaction):
        total = 0
        # This ensures items are loaded if they aren't already
        db.refresh(transaction, attribute_names=['items'])

        for item in transaction.items:
            if item.transaction_type == TransactionType.SELL:
                total += item.total_price
            else: # BUY
                total -= item.total_price
        
        transaction.total_price = total - transaction.discount
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

    def approve(self, db: Session, *, transaction_id: uuid.UUID, current_user: User) -> Transaction:
        transaction = self.get_by_id(db, transaction_id=transaction_id, current_user=current_user, with_items=True)
        
        if current_user.role == UserRole.ADMIN:
            if transaction.status not in [ApprovalStatus.DRAFT, ApprovalStatus.APPROVED_BY_USER]:
                raise AppException(status_code=status.HTTP_400_BAD_REQUEST, detail="This transaction cannot be approved by an admin at its current status.")
            transaction.status = ApprovalStatus.APPROVED_BY_ADMIN
            inventory_service.update_from_transaction(db, transaction=transaction)

        else: # Regular user
            if transaction.status != ApprovalStatus.DRAFT:
                raise AppException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only transactions in 'draft' status can be approved.")
            transaction.status = ApprovalStatus.APPROVED_BY_USER

        db.commit()
        db.refresh(transaction)
        return transaction

    def reject(self, db: Session, *, transaction_id: uuid.UUID, current_user: User) -> Transaction:
        transaction = self.get_by_id(db, transaction_id=transaction_id, current_user=current_user, with_items=True)
        original_status = transaction.status

        if current_user.role == UserRole.ADMIN:
            if transaction.status not in [ApprovalStatus.APPROVED_BY_ADMIN, ApprovalStatus.APPROVED_BY_USER]:
                 raise AppException(status_code=status.HTTP_400_BAD_REQUEST, detail="This transaction cannot be rejected.")
        else: # Regular user
             if transaction.status != ApprovalStatus.APPROVED_BY_USER:
                raise AppException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can only reject transactions you have previously approved.")
        
        transaction.status = ApprovalStatus.DRAFT
        db.add(transaction)
        
        # If the transaction was previously admin approved, its inventory changes must be reversed.
        if original_status == ApprovalStatus.APPROVED_BY_ADMIN:
            inventory_service.revert_from_transaction(db, transaction=transaction)

        db.commit()
        db.refresh(transaction)
        return transaction

transaction_service = TransactionService()

