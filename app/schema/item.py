from pydantic import BaseModel, Field
from typing import Optional
from .base import BaseSchema
from backend.app.models.enums.mesurement import ItemType

# --- Item Schemas ---

class ItemBase(BaseModel):
    name: str = Field(..., max_length=100)
    category: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    type: ItemType = ItemType.UNCOUNTABLE
    karat_default: int = Field(..., ge=0)
    ojrat_default: int = Field(..., ge=0)
    profit_default: int = Field(..., ge=0)
    tax_default: int = Field(..., ge=0)
    is_active: bool = True

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    type: Optional[ItemType] = None
    karat_default: Optional[int] = Field(None, ge=0)
    ojrat_default: Optional[int] = Field(None, ge=0)
    profit_default: Optional[int] = Field(None, ge=0)
    tax_default: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None

class ItemPublic(BaseSchema, ItemBase):
    pass
