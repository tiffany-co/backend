from sqlalchemy.orm import Session
from app.repository.base import BaseRepository
from app.models.inventory import Inventory
from typing import Any

class InventoryRepository(BaseRepository[Inventory, Any, Any]):
    """
    Repository for inventory-related database operations.
    """
    def get_latest(self, db: Session) -> Inventory | None:
        """
        Gets the most recent inventory snapshot from the database.
        """
        return db.query(self.model).order_by(self.model.created_at.desc()).first()

inventory_repo = InventoryRepository(Inventory)

