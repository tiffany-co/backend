from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

from .base import BaseSchema
from ..models.enums.mesurement import MeasurementType
from ..models.enums.transaction import TransactionType

class ItemBase(BaseModel):
    """
    Base schema for item data.
    """
    name: str = Field(..., min_length=2, max_length=100, example="New Gold Jewelry")
    category: str = Field(..., min_length=2, max_length=50, example="Jewelry")
    measurement_type: MeasurementType
    transaction_type: TransactionType
    karat_default: Optional[Decimal] = Field(None, ge=0, example=750.00)
    ojrat_default: Optional[Decimal] = Field(None, ge=0, example=10.50)
    profit_default: Optional[Decimal] = Field(None, ge=0, example=7.00)
    tax_default: Optional[Decimal] = Field(None, ge=0, example=9.00)

class ItemCreate(ItemBase):
    """Schema for creating a new item template."""
    pass

class ItemUpdate(BaseModel):
    """
    Schema for updating an item template. All fields are optional.
    """
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    category: Optional[str] = Field(None, min_length=2, max_length=50)
    measurement_type: Optional[MeasurementType] = None
    transaction_type: Optional[TransactionType] = None
    karat_default: Optional[Decimal] = Field(None, ge=0)
    ojrat_default: Optional[Decimal] = Field(None, ge=0)
    profit_default: Optional[Decimal] = Field(None, ge=0)
    tax_default: Optional[Decimal] = Field(None, ge=0)

class ItemPublic(ItemBase, BaseSchema):
    """
    Schema for publicly available item information.
    """
    class Config:
        from_attributes = True

