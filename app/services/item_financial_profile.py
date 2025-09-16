from sqlalchemy.orm import Session
import uuid

from app.core.exceptions import AppException
from fastapi import status
from app.models.user import User
from app.models.item_financial_profile import ItemFinancialProfile
from app.repository.item_financial_profile import item_financial_profile_repo
from app.schema.item_financial_profile import ItemFinancialProfileUpdate
from app.logging_config import audit_logger

class ItemFinancialProfileService:
    """
    Service layer for item financial profile business logic.
    """
    def get_by_id(self, db: Session, *, profile_id: uuid.UUID) -> ItemFinancialProfile:
        """Helper method to get a profile by ID or raise 404."""
        profile = item_financial_profile_repo.get(db, id=profile_id)
        if not profile:
            raise AppException(status_code=status.HTTP_404_NOT_FOUND, detail="Financial profile not found.")
        return profile

    def update(self, db: Session, *, profile_id: uuid.UUID, profile_in: ItemFinancialProfileUpdate, current_user: User) -> ItemFinancialProfile:
        """Update a financial profile."""
        profile_to_update = self.get_by_id(db, profile_id=profile_id)
        updated_profile = item_financial_profile_repo.update(db, db_obj=profile_to_update, obj_in=profile_in)
        audit_logger.info(f"Financial profile ID '{profile_id}' for item '{profile_to_update.item.name}' updated by '{current_user.username}'.")
        return updated_profile

item_financial_profile_service = ItemFinancialProfileService()

