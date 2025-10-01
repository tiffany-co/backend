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
    investor_id: Optional[uuid.UUID] = None
    transaction_id: Optional[uuid.UUID] = None
    account_ledger_id: Optional[uuid.UUID] = None
    saved_bank_account_id: Optional[uuid.UUID] = None
    contact_id: Optional[uuid.UUID] = None

class PaymentCreate(PaymentBase):
    """Schema for creating a new payment."""

    @model_validator(mode='before')
    @classmethod
    def validate_payment_logic(cls, data: Any):
        """
        Ensures the combination of fields is logical based on the payment direction.
        """
        if not isinstance(data, dict):
            return data

        direction = data.get("direction")
        investor_id = data.get("investor_id")
        transaction_id = data.get("transaction_id")

        if investor_id and transaction_id:
            raise ValueError("A payment can be linked to an investor or a transaction, but not both.")

        if direction == PaymentDirection.INCOMING:
            if data.get("account_ledger_id"):
                raise ValueError("Incoming payments cannot be linked to an account ledger.")
        
        elif direction == PaymentDirection.INTERNAL_TRANSFER:
            if not data.get("account_ledger_id"):
                raise ValueError("Internal transfers must be linked to an account ledger.")
            if data.get("saved_bank_account_id"):
                raise ValueError("Internal transfers cannot be linked to a saved bank account.")
        
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

