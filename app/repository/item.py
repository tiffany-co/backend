from app.models.item import Item
from app.schema.item import ItemCreate, ItemUpdate
from .base import BaseRepository

class ItemRepository(BaseRepository[Item, ItemCreate, ItemUpdate]):
    """
    Repository for Item model operations.
    """
    pass

# Create a single, importable instance of the repository.
item_repo = ItemRepository(Item)
