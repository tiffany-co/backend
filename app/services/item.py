from sqlalchemy.orm import Session
import uuid
from typing import List

from app.core.exceptions import AppException
from fastapi import status
from app.models.user import User
from app.models.item import Item
from app.repository.item import item_repo
from app.schema.item import ItemUpdate
from app.logging_config import audit_logger

class ItemService:
    """
    Service layer for item business logic.
    """
    def get_by_id(self, db: Session, *, item_id: uuid.UUID) -> Item:
        """Helper method to get an item by ID or raise 404."""
        item = item_repo.get(db, id=item_id)
        if not item:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found.",
            )
        return item

    def get_all(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Item]:
        """Get all items."""
        return item_repo.get_multi(db, skip=skip, limit=limit)

    def update(self, db: Session, *, item_id: uuid.UUID, item_in: ItemUpdate, current_user: User) -> Item:
        """Update an item's metadata."""
        item_to_update = self.get_by_id(db, item_id=item_id)
        
        updated_item = item_repo.update(db, db_obj=item_to_update, obj_in=item_in)
        audit_logger.info(f"Item '{updated_item.name}' updated by user '{current_user.username}'.")
        return updated_item

item_service = ItemService()
