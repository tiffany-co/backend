from app.models.saved_bank_account import SavedBankAccount
from app.schema.saved_bank_account import SavedBankAccountCreate, SavedBankAccountUpdate
from .base import BaseRepository

class SavedBankAccountRepository(
    BaseRepository[SavedBankAccount, SavedBankAccountCreate, SavedBankAccountUpdate]
):
    """
    Repository for SavedBankAccount model operations.
    """
    pass

# Create a single, importable instance of the repository.
saved_bank_account_repo = SavedBankAccountRepository(SavedBankAccount)
