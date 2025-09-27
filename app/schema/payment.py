import uuid
from datetime import datetime
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Any

from .base import BaseSchema
from ..models.enums.payment import PaymentMethod, PaymentDirection
from ..models.enums.shared import ApprovalStatus

class PaymentBase(BaseModel):
    """Base schema for payment data."""
    amount: int = Field(..., gt=0, description="The amount of the payment in Iranian Rials.")
    payment_method: PaymentMethod
    direction: PaymentDirection
    description: Optional[str] = Field(None, max_length=500)
    photo_holder_id: Optional[uuid.UUID] = Field(None, description="ID of the user holding the receipt photo.")

    # Linkages
    investment_id: Optional[uuid.UUID] = None
    transaction_id: Optional[uuid.UUID] = None
    account_ledger_id: Optional[uuid.UUID] = None
    saved_bank_account_id: Optional[uuid.UUID] = None
    contact_id: Optional[uuid.UUID] = None

class PaymentCreate(PaymentBase):
    """Schema for creating a new payment."""

    @model_validator(mode='before')
    @classmethod
    def check_exclusive_links(cls, data: Any):
        """
        Ensure that for each pair of mutually exclusive fields, exactly one is provided.
        """
        if not isinstance(data, dict):
            return data

        # Check that exactly one of transaction_id or investment_id is set
        has_transaction = data.get("transaction_id") is not None
        has_investment = data.get("investment_id") is not None
        if not (has_transaction ^ has_investment): # XOR: one must be true, not both or neither
            raise ValueError("A payment must be linked to exactly one of a transaction or an investment.")

        # Check that exactly one of account_ledger_id or saved_bank_account_id is set
        has_ledger = data.get("account_ledger_id") is not None
        has_bank = data.get("saved_bank_account_id") is not None
        if not (has_ledger ^ has_bank): # XOR: one must be true, not both or neither
            raise ValueError("A payment must be linked to exactly one of an account ledger or a saved bank account.")
            
        return data

class PaymentUpdate(BaseModel):
    """Schema for updating a payment. All fields are optional."""
    amount: Optional[int] = Field(None, gt=0)
    payment_method: Optional[PaymentMethod] = None
    direction: Optional[PaymentDirection] = None
    description: Optional[str] = Field(None, max_length=500)
    photo_holder_id: Optional[uuid.UUID] = None

class PaymentPublic(PaymentBase, BaseSchema):
    """Schema for public representation of a payment."""
    recorder_id: uuid.UUID
    status: ApprovalStatus

    class Config:
        from_attributes = True

