import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

from .base import BaseSchema

class AccountLedgerBase(BaseModel):
    """Base schema for account ledger data."""
    contact_id: uuid.UUID = Field(..., description="The ID of the contact this ledger entry belongs to.")
    transaction_id: Optional[uuid.UUID] = Field(None, description="The ID of the associated transaction, if any.")
    debt: int = Field(..., description="Amount in Rials. The amount we owe the customer.")
    deadline: Optional[datetime] = Field(None, description="The date by which the debt should be settled.")
    description: Optional[str] = Field(None, max_length=500)
    card_number: Optional[str] = Field(None, max_length=24)
    bank_name: Optional[str] = Field(None, max_length=50)

class AccountLedgerCreate(AccountLedgerBase):
    """Schema for creating a new account ledger entry."""
    pass

class AccountLedgerUpdate(BaseModel):
    """Schema for updating an account ledger entry. All fields are optional."""
    debt: Optional[int] = Field(None)
    deadline: Optional[datetime] = Field(None)
    description: Optional[str] = Field(None, max_length=500)
    card_number: Optional[str] = Field(None, max_length=24)
    bank_name: Optional[str] = Field(None, max_length=50)

class AccountLedgerPublic(BaseSchema, AccountLedgerBase):
    """Schema for representing an account ledger entry in public API responses."""
    class Config:
        from_attributes = True
