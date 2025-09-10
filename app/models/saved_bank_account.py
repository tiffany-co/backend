from sqlalchemy import Column, String, Text
from app.models.base import BaseModel

class SavedBankAccount(BaseModel):
    """
    Represents a saved bank account in the system.
    This model maps to the 'saved_bank_account' table.
    """
    __tablename__ = "saved_bank_account"

    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    card_number = Column(String, nullable=True, unique=True, index=True)

    def __repr__(self):
        return f"<SavedBankAccount(id={self.id}, name='{self.name}')>"
