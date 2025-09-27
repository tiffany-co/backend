from sqlalchemy.orm import Session
from typing import Dict, Any, List
from sqlalchemy.inspection import inspect

from app.models.user import User
from app.models.inventory import Inventory
from app.models.transaction import Transaction
from app.models.payment import Payment
from app.models.enums.transaction import TransactionType
from app.models.enums.payment import PaymentDirection
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

        new_snapshot_data = self._get_new_snapshot_base(latest_inventory)

        # Apply adjustments
        if adjustment_in.money_balance is not None:
            new_snapshot_data["money_balance"] = adjustment_in.money_balance

        if adjustment_in.inventory:
            new_snapshot_data.update(adjustment_in.inventory.model_dump(exclude_unset=True))

        new_snapshot_data["description"] = adjustment_in.description

        # Persist new snapshot
        new_record = inventory_repo.create(db, obj_in=new_snapshot_data)

        return _format_inventory(new_record)

    def update_from_transaction(self, db: Session, *, transaction: Transaction):
        """Creates a new inventory snapshot based on an approved transaction's item changes."""
        new_snapshot_data = self._calculate_new_snapshot_from_transaction(db, transaction, is_reversal=False)
        new_snapshot_data["description"] = f"INVENTORY UPDATE FROM TRANSACTION {transaction.id}"
        new_snapshot_data["transaction_id"] = transaction.id
        inventory_repo.create(db, obj_in=new_snapshot_data)

    def revert_from_transaction(self, db: Session, *, transaction: Transaction):
        """Creates a new inventory snapshot that reverses a previously approved transaction's item changes."""
        new_snapshot_data = self._calculate_new_snapshot_from_transaction(db, transaction, is_reversal=True)
        new_snapshot_data["description"] = f"REVERSAL OF INVENTORY UPDATE FROM TRANSACTION {transaction.id}"
        new_snapshot_data["transaction_id"] = transaction.id
        inventory_repo.create(db, obj_in=new_snapshot_data)

    def update_money_balance_from_payment(self, db: Session, *, payment: Payment):
        """Creates a new inventory snapshot based on a payment's money movement."""
        new_snapshot_data = self._calculate_new_snapshot_from_payment(db, payment, is_reversal=False)
        new_snapshot_data["description"] = f"MONEY BALANCE UPDATE FROM PAYMENT {payment.id}"
        new_snapshot_data["payment_id"] = payment.id
        inventory_repo.create(db, obj_in=new_snapshot_data)

    def revert_money_balance_from_payment(self, db: Session, *, payment: Payment):
        """Creates a new snapshot that reverses a payment's money movement."""
        new_snapshot_data = self._calculate_new_snapshot_from_payment(db, payment, is_reversal=True)
        new_snapshot_data["description"] = f"REVERSAL OF MONEY BALANCE UPDATE FROM PAYMENT {payment.id}"
        new_snapshot_data["payment_id"] = payment.id
        inventory_repo.create(db, obj_in=new_snapshot_data)
        
    def _get_new_snapshot_base(self, latest_inventory: Inventory | None) -> Dict[str, Any]:
        """Gets the state of the last inventory, or a zeroed-out state if none exists."""
        if latest_inventory:
            return _extract_model_attrs(
                latest_inventory, exclude=["id", "created_at", "updated_at", "transaction_id", "payment_id"]
            )
        
        # If no inventory exists, create a zeroed-out base
        base = {item.value: 0 for item in ItemType}
        base['money_balance'] = 0
        return base

    def _calculate_new_snapshot_from_transaction(self, db: Session, transaction: Transaction, is_reversal: bool) -> Dict[str, Any]:
        """Calculates the next inventory state from a transaction's items."""
        latest_inventory = inventory_repo.get_latest(db)
        new_snapshot_data = self._get_new_snapshot_base(latest_inventory)

        for trans_item in transaction.items:
            item_key = trans_item.item.name
            if item_key in new_snapshot_data:
                # If it's a reversal, flip the logic
                if is_reversal:
                    if trans_item.transaction_type == TransactionType.SELL:
                        new_snapshot_data[item_key] += trans_item.weight_count  # Add back
                    else:  # BUY
                        new_snapshot_data[item_key] -= trans_item.weight_count  # Remove
                else: # The transaction was successful
                    if trans_item.transaction_type == TransactionType.SELL:
                        new_snapshot_data[item_key] -= trans_item.weight_count
                    else:  # BUY
                        new_snapshot_data[item_key] += trans_item.weight_count
        
        return new_snapshot_data

    def _calculate_new_snapshot_from_payment(self, db: Session, payment: Payment, is_reversal: bool) -> Dict[str, Any]:
        """Calculates the next inventory state from a payment's money movement."""
        latest_inventory = inventory_repo.get_latest(db)
        new_snapshot_data = self._get_new_snapshot_base(latest_inventory)

        amount = payment.amount
        
        # If it's a reversal, flip the logic
        if is_reversal:
            if payment.direction == PaymentDirection.INCOMING:
                new_snapshot_data["money_balance"] -= amount # Take money back out
            elif payment.direction == PaymentDirection.OUTGOING:
                new_snapshot_data["money_balance"] += amount # Put money back in
        else: # The payment was successful
            if payment.direction == PaymentDirection.INCOMING:
                new_snapshot_data["money_balance"] += amount
            elif payment.direction == PaymentDirection.OUTGOING:
                new_snapshot_data["money_balance"] -= amount
        
        # INTERNAL_TRANSFER has no effect on money_balance
        return new_snapshot_data

inventory_service = InventoryService()

