from sqlalchemy.orm import Session
from app.models.saved_bank_account import SavedBankAccount
from app.repository.saved_bank_account import saved_bank_account_repo
from app.schema.saved_bank_account import SavedBankAccountCreate, SavedBankAccountUpdate

class SavedBankAccountService:
    """
    Service layer for saved bank account business logic.
    For now, it's a simple pass-through to the repository.
    """

    def create(self, db: Session, *, obj_in: SavedBankAccountCreate) -> SavedBankAccount:
        return saved_bank_account_repo.create(db, obj_in=obj_in)

    def update(
        self, db: Session, *, db_obj: SavedBankAccount, obj_in: SavedBankAccountUpdate
    ) -> SavedBankAccount:
        return saved_bank_account_repo.update(db, db_obj=db_obj, obj_in=obj_in)

# Create a single, importable instance of the service.
saved_bank_account_service = SavedBankAccountService()
