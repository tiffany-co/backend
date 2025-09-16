from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
import uuid

from .base import BaseSchema
from ..models.enums.transaction import TransactionType

class ItemFinancialProfileBase(BaseModel):
    """Base schema for an item's financial profile."""
    transaction_type: TransactionType
    karat_default: Optional[Decimal] = Field(None, ge=0, example=900.00)
    ojrat_default: Optional[Decimal] = Field(None, ge=0, example=0.00)
    profit_default: Optional[Decimal] = Field(None, ge=0, example=2.50)
    tax_default: Optional[Decimal] = Field(None, ge=0, example=0.00)

class ItemFinancialProfileInList(ItemFinancialProfileBase):
    """
    Schema for representing a financial profile in a list view.
    Excludes timestamps.
    """
    id: uuid.UUID

    class Config:
        from_attributes = True
        
class ItemFinancialProfileCreate(ItemFinancialProfileBase):
    """Schema for creating a new financial profile for an item."""
    pass

class ItemFinancialProfilePublic(ItemFinancialProfileBase, BaseSchema):
    """Schema for publicly available financial profile information."""
    class Config:
        from_attributes = True

class ItemFinancialProfileUpdate(BaseModel):
    """Schema for updating a financial profile's defaults. All fields are optional."""
    karat_default: Optional[Decimal] = Field(None, ge=0)
    ojrat_default: Optional[Decimal] = Field(None, ge=0)
    profit_default: Optional[Decimal] = Field(None, ge=0)
    tax_default: Optional[Decimal] = Field(None, ge=0)

