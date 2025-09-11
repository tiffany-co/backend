from sqlalchemy.orm import Session
import uuid
from typing import List

from app.core.exceptions import AppException
from fastapi import status
from app.models.user import User
from app.models.item import Item
from app.repository.item import item_repo
from app.schema.item import ItemCreate, ItemUpdate
from app.logging_config import audit_logger

class ItemService:
    """
    Service layer for item template business logic.
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
        """Get all item templates."""
        return item_repo.get_multi(db, skip=skip, limit=limit)
    
    def create(self, db: Session, *, item_in: ItemCreate, current_user: User) -> Item:
        """Create a new item template with validation."""
        if item_repo.get_by_name(db, name=item_in.name):
            raise AppException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"An item with the name '{item_in.name}' already exists.",
            )
        
        new_item = item_repo.create(db, obj_in=item_in)
        audit_logger.info(f"Item Template '{new_item.name}' created by user '{current_user.username}'.")
        return new_item

    def update(self, db: Session, *, item_id: uuid.UUID, item_in: ItemUpdate, current_user: User) -> Item:
        """Update an item template with validation."""
        item_to_update = self.get_by_id(db, item_id=item_id)
        
        if item_in.name and item_in.name != item_to_update.name:
            existing = item_repo.get_by_name(db, name=item_in.name)
            if existing and existing.id != item_to_update.id:
                 raise AppException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Another item with the name '{item_in.name}' already exists.",
                )

        updated_item = item_repo.update(db, db_obj=item_to_update, obj_in=item_in)
        audit_logger.info(f"Item Template '{updated_item.name}' updated by user '{current_user.username}'.")
        return updated_item

    def delete(self, db: Session, *, item_id: uuid.UUID, current_user: User) -> Item:
        """Delete an item template."""
        item_to_delete = self.get_by_id(db, item_id=item_id)
        deleted_item = item_repo.remove(db, id=item_id)
        audit_logger.info(f"Item Template '{item_to_delete.name}' deleted by user '{current_user.username}'.")
        return deleted_item

item_service = ItemService()

