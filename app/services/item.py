from sqlalchemy.orm import Session
import uuid
from typing import List, Optional

from app.core.exceptions import AppException
from fastapi import status
from app.models.user import User
from app.models.item import Item, MeasurementType
from app.repository.item import item_repo
from app.schema.item import ItemUpdate, ItemInListWithProfiles

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

    def update(self, db: Session, *, item_id: uuid.UUID, item_in: ItemUpdate) -> Item:
        """Update an item's metadata."""
        item_to_update = self.get_by_id(db, item_id=item_id)
        
        updated_item = item_repo.update(db, db_obj=item_to_update, obj_in=item_in)
        return updated_item
    
    def search(
        self,
        db: Session,
        *,
        name_fa: Optional[str] = None,
        category: Optional[str] = None,
        measurement_type: Optional[MeasurementType] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[ItemInListWithProfiles]:
        """Searches for items using the repository."""
        return item_repo.search(
            db,
            name_fa=name_fa,
            category=category,
            measurement_type=measurement_type,
            is_active=is_active,
            skip=skip,
            limit=limit
        )

item_service = ItemService()
