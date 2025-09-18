from sqlalchemy.orm import Session
from typing import Dict, Any, List

from app.core.exceptions import AppException
from fastapi import status
from app.models.user import User
from app.models.inventory import Inventory
from app.models.enums.item_type import ItemType
from app.repository.inventory import inventory_repo
from app.repository.item import item_repo
from app.schema.inventory import InventoryAdjust
from app.logging_config import audit_logger
from sqlalchemy.inspection import inspect

def model_to_dict(obj: Any) -> Dict[str, Any]:
    """Convert a SQLAlchemy model instance to a dictionary, including only its columns."""
    if not obj:
        return {}
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

class InventoryService:
    """Service layer for inventory business logic."""

    def get_all_history(self, db: Session, skip: int, limit: int) -> List[Inventory]:
        return inventory_repo.get_multi(db, skip=skip, limit=limit)

    def get_current_balance(self, db: Session) -> Dict[str, Any]:
        """
        Gets the current inventory balance, formatted in the standard nested structure.
        """
        latest_inventory = inventory_repo.get_latest(db)
        if not latest_inventory:
            zero_inventory = {item.value: 0 for item in ItemType}
            return {"money_balance": 0, "inventory": zero_inventory}

        balance_dict = model_to_dict(latest_inventory)
        money_balance = balance_dict.pop("money_balance", 0)
        
        for key in ['id', 'created_at', 'updated_at', 'description']:
            balance_dict.pop(key, None)
            
        return {"money_balance": money_balance, "inventory": balance_dict}

    def get_current_balance_fa(self, db: Session) -> Dict[str, Any]:
        """
        Gets the current inventory balance with Persian display names.
        """
        raw_balance = self.get_current_balance(db)
        
        all_items = item_repo.get_multi(db, limit=1000)
        item_map = {item.name: item.name_fa for item in all_items}

        translated_inventory = {
            item_map.get(key, key): value
            for key, value in raw_balance.get("inventory", {}).items()
        }
        return {"money_balance": raw_balance["money_balance"], "inventory": translated_inventory}


    def adjust_inventory(self, db: Session, *, adjustment_in: InventoryAdjust, current_user: User) -> Inventory:
        """Creates a new inventory snapshot based on a manual adjustment."""
        latest = inventory_repo.get_latest(db)
        
        new_snapshot_data = model_to_dict(latest) if latest else {}

        for key in ['id', 'created_at', 'updated_at']:
            new_snapshot_data.pop(key, None)

        # --- UPDATED: Apply adjustments from the consistent, nested structure ---
        if adjustment_in.money_balance is not None:
            new_snapshot_data['money_balance'] = adjustment_in.money_balance
        
        if adjustment_in.inventory:
            inventory_adjustments = adjustment_in.inventory.model_dump(exclude_unset=True)
            for key, value in inventory_adjustments.items():
                if key in new_snapshot_data:
                    new_snapshot_data[key] = value
        
        new_snapshot_data["description"] = adjustment_in.description

        new_inventory_record = inventory_repo.create(db, obj_in=new_snapshot_data)
        
        audit_logger.info(f"Manual inventory adjustment by '{current_user.username}'. Note: {adjustment_in.description}")
        return new_inventory_record

inventory_service = InventoryService()

