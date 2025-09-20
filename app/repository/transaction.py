from typing import Any
from app.repository.base import BaseRepository
from app.models.transaction import Transaction

class TransactionRepository(BaseRepository[Transaction, Any, Any]):
    """
    Repository for Transaction model operations.
    Inherits from BaseRepository for standard CRUD.
    """
    pass

transaction_repo = TransactionRepository(Transaction)
