from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
import uuid

from .base import BaseSchema
from ..models.enums.measurement import MeasurementType
from .item_financial_profile import ItemFinancialProfilePublic, ItemFinancialProfileUpdate, ItemFinancialProfileInList
# --- Base and Public Schemas ---

class ItemBase(BaseModel):
    """Base schema for core item data."""
    name: str = Field(..., json_schema_extra={"example": "Emami Coin"})
    name_fa: str = Field(..., json_schema_extra={"example": "سکه امامی"})
    category: str = Field(..., json_schema_extra={"example": "Coin"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "Standard Emami gold coins."})
    measurement_type: MeasurementType
    is_active: bool = Field(True)

class ItemCreate(ItemBase):
    """Schema for creating a new item (used by seeder)."""
    pass

# --- Schemas for different API responses ---
class ItemInList(ItemBase):
    """
    Schema for representing an item in a list view.
    Excludes timestamps for a cleaner response.
    """
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

class ItemPublic(ItemBase, BaseSchema):
    """
    Schema for representing a single, detailed item, including timestamps.
    """
    model_config = ConfigDict(from_attributes=True)

class ItemWithProfilesPublic(ItemPublic):
    """
    A detailed schema for an item that also includes its nested financial profiles.
    """
    financial_profiles: List[ItemFinancialProfilePublic] = []

class ItemInListWithProfiles(ItemInList):
    """A schema for the item list view that includes financial profiles but no timestamps."""
    financial_profiles: List[ItemFinancialProfileInList] = []

# --- Schema for Updating ---

class ItemUpdate(BaseModel):
    """Schema for updating an item's core identity. All fields are optional."""
    name_fa: Optional[str] = Field(None, json_schema_extra={"example": "سکه امامی طرح جدید"})
    category: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    is_active: Optional[bool] = Field(None)
