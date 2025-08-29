# app/services/item.py

from sqlalchemy.orm import Session
from app.models.item import Item
from app.repository.item import item_repo
from app.schema.item import ItemCreate, ItemUpdate

class ItemService:
    """
    Service layer for item-related business logic.
    """

    def create(self, db: Session, *, obj_in: ItemCreate) -> Item:
        return item_repo.create(db, obj_in=obj_in)

    def update(self, db: Session, *, db_obj: Item, obj_in: ItemUpdate) -> Item:
        return item_repo.update(db, db_obj=db_obj, obj_in=obj_in)

# Create a single, importable instance of the service.
item_service = ItemService()
