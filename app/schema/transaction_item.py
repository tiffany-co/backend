import uuid
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

from .base import BaseSchema
from app.models.enums.transaction import TransactionType

class TransactionItemBase(BaseModel):
    transaction_id: uuid.UUID
    item_id: uuid.UUID
    transaction_type: TransactionType
    title: str = Field(..., min_length=1)
    weight_count: Decimal = Field(..., gt=0)
    unit_price: int = Field(..., ge=0)
    karat: Optional[Decimal] = Field(None, ge=0)
    ojrat: Optional[Decimal] = Field(None, ge=0)
    profit: Optional[Decimal] = Field(None, ge=0)
    tax: Optional[Decimal] = Field(None, ge=0)

class TransactionItemCreate(TransactionItemBase):
    pass

class TransactionItemUpdate(BaseModel):
    item_id: Optional[uuid.UUID] = None
    transaction_type: Optional[TransactionType] = None
    title: Optional[str] = Field(None, min_length=1)
    weight_count: Optional[Decimal] = Field(None, gt=0)
    unit_price: Optional[int] = Field(None, ge=0)
    karat: Optional[Decimal] = Field(None, ge=0)
    ojrat: Optional[Decimal] = Field(None, ge=0)
    profit: Optional[Decimal] = Field(None, ge=0)
    tax: Optional[Decimal] = Field(None, ge=0)

class TransactionItemPublic(BaseSchema):
    transaction_id: uuid.UUID
    item_id: uuid.UUID
    transaction_type: TransactionType
    title: str
    weight_count: Decimal
    unit_price: int
    total_price: int
    karat: Optional[Decimal]
    ojrat: Optional[Decimal]
    profit: Optional[Decimal]
    tax: Optional[Decimal]

    class Config:
        from_attributes = True
