from pydantic import BaseModel, Field
from typing import Optional
from .base import BaseSchema

# --- Saved Bank Account Schemas ---

# Base properties for a saved bank account.
class SavedBankAccountBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=255)

# Properties required for creating a new bank account.
class SavedBankAccountCreate(SavedBankAccountBase):
    pass

# Properties allowed for updating a bank account. All fields are optional.
class SavedBankAccountUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=255)

# Public representation of a SavedBankAccount.
class SavedBankAccountPublic(BaseSchema, SavedBankAccountBase):
    pass
