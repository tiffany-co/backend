from sqlalchemy.orm import Session
from app.repository.base import BaseRepository
from app.models.item import Item
from app.schema.item import ItemCreate, ItemUpdate

class ItemRepository(BaseRepository[Item, ItemCreate, ItemUpdate]):
    """
    Repository for item-related database operations.
    """
    def get_by_name(self, db: Session, *, name: str) -> Item | None:
        """Get an item by its unique name."""
        return db.query(self.model).filter(self.model.name == name).first()

item_repo = ItemRepository(Item)

