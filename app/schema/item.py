from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

from .base import BaseSchema
from backend.app.models.enums.measurement import MeasurementType
from app.models.enums.transaction import TransactionType

class ItemBase(BaseModel):
    """
    Base schema for item data.
    """
    name: str = Field(..., min_length=2, max_length=100)
    category: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    is_active: bool = Field(True)
    inventory_column_name: str = Field(...)
    display_name_fa: str = Field(...)
    measurement_type: MeasurementType
    transaction_type: TransactionType
    karat_default: Optional[Decimal] = Field(None, ge=0)
    ojrat_default: Optional[Decimal] = Field(None, ge=0)
    profit_default: Optional[Decimal] = Field(None, ge=0)
    tax_default: Optional[Decimal] = Field(None, ge=0)

class ItemCreate(ItemBase):
    """Schema for creating a new item template (used by seeder)."""
    pass

class ItemUpdate(BaseModel):
    """
    Schema for updating an item template. All fields are optional.
    """
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    category: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = Field(None) # Added is_active
    display_name_fa: Optional[str] = Field(None)
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

