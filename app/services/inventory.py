from sqlalchemy.orm import Session
from typing import Dict, Any, List
from sqlalchemy.inspection import inspect

from app.models.user import User
from app.models.inventory import Inventory
from app.models.enums.item_type import ItemType
from app.repository.inventory import inventory_repo
from app.schema.inventory import InventoryAdjust

# --- Helpers ---
def _extract_model_attrs(model: Any, exclude: List[str] = None) -> Dict[str, Any]:
    """Extracts SQLAlchemy model attributes into a dict, excluding some fields."""
    exclude = exclude or []
    return {
        c.key: getattr(model, c.key)
        for c in inspect(model).mapper.column_attrs
        if c.key not in exclude
    }


def _format_inventory(inventory: Inventory | None) -> Dict[str, Any]:
    """
    Converts an Inventory SQLAlchemy model into a nested dictionary.
    Returns a zero-filled response if no inventory exists.
    """
    if not inventory:
        return {
            "money_balance": 0,
            "inventory": {item.value: 0 for item in ItemType},
            "description": "No inventory history found."
        }

    inventory_dict = _extract_model_attrs(inventory)

    # Separate item fields from metadata
    item_keys = {item.value for item in ItemType}
    inventory_items = {k: v for k, v in inventory_dict.items() if k in item_keys}

    return {
        "id": inventory.id,
        "created_at": inventory.created_at,
        "updated_at": inventory.updated_at,
        "description": inventory.description,
        "money_balance": inventory.money_balance,
        "inventory": inventory_items,
    }


# --- Service Layer ---
class InventoryService:
    """Service layer for inventory-related business logic."""

    def get_all_history(self, db: Session, skip: int, limit: int) -> List[Dict[str, Any]]:
        """Retrieve and format the full history of inventory snapshots."""
        history = inventory_repo.get_multi(db, skip=skip, limit=limit)
        return [_format_inventory(snapshot) for snapshot in history]

    def get_current_balance(self, db: Session) -> Dict[str, Any]:
        """Retrieve and format the latest inventory snapshot."""
        return _format_inventory(inventory_repo.get_latest(db))

    def adjust_inventory(self, db: Session, *, adjustment_in: InventoryAdjust) -> Dict[str, Any]:
        """Create a new inventory snapshot based on manual adjustments."""
        latest_inventory = inventory_repo.get_latest(db)

        # Start with previous snapshot or empty
        new_snapshot_data = _extract_model_attrs(
            latest_inventory,
            exclude=["id", "created_at", "updated_at"]
        ) if latest_inventory else {}

        # Apply adjustments
        if adjustment_in.money_balance is not None:
            new_snapshot_data["money_balance"] = adjustment_in.money_balance

        if adjustment_in.inventory:
            new_snapshot_data.update(adjustment_in.inventory.model_dump(exclude_unset=True))

        new_snapshot_data["description"] = adjustment_in.description

        # Persist new snapshot
        new_record = inventory_repo.create(db, obj_in=new_snapshot_data)

        return _format_inventory(new_record)


inventory_service = InventoryService()
