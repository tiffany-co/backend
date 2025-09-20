from typing import Any
from app.repository.base import BaseRepository
from app.models.transaction_item import TransactionItem

class TransactionItemRepository(BaseRepository[TransactionItem, Any, Any]):
    """
    Repository for TransactionItem model operations.
    Inherits from BaseRepository for standard CRUD.
    """
    pass

transaction_item_repo = TransactionItemRepository(TransactionItem)
