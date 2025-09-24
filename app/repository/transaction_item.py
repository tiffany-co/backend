from app.repository.base import BaseRepository, CreateSchemaType, UpdateSchemaType
from app.models.transaction_item import TransactionItem

class TransactionItemRepository(BaseRepository[TransactionItem, CreateSchemaType, UpdateSchemaType]):
    """
    Repository for TransactionItem model operations.
    Inherits from BaseRepository for standard CRUD.
    """
    pass

transaction_item_repo = TransactionItemRepository(TransactionItem)

