from sqlalchemy.orm import Session
import uuid
from typing import List

from app.core.exceptions import AppException
from fastapi import status
from app.models.user import User
from app.models.saved_bank_account import SavedBankAccount
from app.repository.saved_bank_account import saved_bank_account_repo
from app.schema.saved_bank_account import SavedBankAccountCreate, SavedBankAccountUpdate
from app.logging_config import audit_logger

class SavedBankAccountService:
    """
    Service layer for saved bank account business logic.
    """
    def get_by_id(self, db: Session, *, account_id: uuid.UUID) -> SavedBankAccount:
        """Helper method to get an account by ID or raise 404."""
        account = saved_bank_account_repo.get(db, id=account_id)
        if not account:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Saved bank account with ID {account_id} not found.",
            )
        return account

    def get_all(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[SavedBankAccount]:
        """Get all saved bank accounts."""
        return saved_bank_account_repo.get_multi(db, skip=skip, limit=limit)
    
    def create(self, db: Session, *, account_in: SavedBankAccountCreate, current_user: User) -> SavedBankAccount:
        """Create a new saved bank account with validation."""
        if saved_bank_account_repo.get_by_name(db, name=account_in.name):
            raise AppException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A bank account with the name '{account_in.name}' already exists.",
            )
        if account_in.card_number and saved_bank_account_repo.get_by_card_number(db, card_number=account_in.card_number):
            raise AppException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A bank account with this card number already exists.",
            )
        
        new_account = saved_bank_account_repo.create(db, obj_in=account_in)
        audit_logger.info(f"Bank Account '{new_account.name}' created by user '{current_user.username}'.")
        return new_account

    def update(self, db: Session, *, account_id: uuid.UUID, account_in: SavedBankAccountUpdate, current_user: User) -> SavedBankAccount:
        """Update a saved bank account with validation."""
        account_to_update = self.get_by_id(db, account_id=account_id)
        
        if account_in.name:
            existing = saved_bank_account_repo.get_by_name(db, name=account_in.name)
            if existing and existing.id != account_to_update.id:
                 raise AppException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Another bank account with the name '{account_in.name}' already exists.",
                )
        if account_in.card_number:
            existing = saved_bank_account_repo.get_by_card_number(db, card_number=account_in.card_number)
            if existing and existing.id != account_to_update.id:
                raise AppException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Another bank account with this card number already exists.",
                )

        updated_account = saved_bank_account_repo.update(db, db_obj=account_to_update, obj_in=account_in)
        audit_logger.info(f"Bank Account '{updated_account.name}' updated by user '{current_user.username}'.")
        return updated_account

    def delete(self, db: Session, *, account_id: uuid.UUID, current_user: User) -> SavedBankAccount:
        """Delete a saved bank account."""
        account_to_delete = self.get_by_id(db, account_id=account_id)
        deleted_account = saved_bank_account_repo.remove(db, id=account_id)
        audit_logger.info(f"Bank Account '{account_to_delete.name}' deleted by user '{current_user.username}'.")
        return deleted_account

saved_bank_account_service = SavedBankAccountService()

