from sqlalchemy.orm import Session
from typing import List, Optional

from app.repository.base import BaseRepository
from app.models.item import Item, MeasurementType
from app.schema.item import ItemCreate, ItemUpdate, ItemInListWithProfiles

class ItemRepository(BaseRepository[Item, ItemCreate, ItemUpdate]):
    """
    Repository for item-related database operations.
    """
    def get_by_name(self, db: Session, *, name: str) -> Item | None:
        """Get an item by its unique name."""
        return db.query(self.model).filter(self.model.name == name).first()

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
        """
        Searches for items based on a combination of criteria.
        """
        query = db.query(self.model)
        
        if name_fa:
            query = query.filter(self.model.name_fa.ilike(f"%{name_fa}%"))
        if category:
            query = query.filter(self.model.category.ilike(f"%{category}%"))
        if measurement_type:
            query = query.filter(self.model.measurement_type == measurement_type)
        if is_active is not None:
            query = query.filter(self.model.is_active == is_active)
            
        return query.offset(skip).limit(limit).all()

item_repo = ItemRepository(Item)

