from sqlalchemy.orm import Session
from app.repository.base import BaseRepository
from app.models.saved_bank_account import SavedBankAccount
from app.schema.saved_bank_account import SavedBankAccountCreate, SavedBankAccountUpdate

class SavedBankAccountRepository(BaseRepository[SavedBankAccount, SavedBankAccountCreate, SavedBankAccountUpdate]):
    """
    Repository for saved bank account related database operations.
    """
    def get_by_name(self, db: Session, *, name: str) -> SavedBankAccount | None:
        """Get a saved bank account by its name."""
        return db.query(self.model).filter(self.model.name == name).first()
    
    def get_by_card_number(self, db: Session, *, card_number: str) -> SavedBankAccount | None:
        """Get a saved bank account by its card number."""
        return db.query(self.model).filter(self.model.card_number == card_number).first()

saved_bank_account_repo = SavedBankAccountRepository(SavedBankAccount)

