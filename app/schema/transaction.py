import uuid
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from .base import BaseSchema
from app.models.enums.transaction import TransactionStatus
from .transaction_item import TransactionItemPublic
from .user import UserPublic
from .contact import ContactPublic

# --- Base Schemas ---

class TransactionBase(BaseModel):
    contact_id: uuid.UUID
    note: Optional[str] = None
    discount: int = Field(0, ge=0)

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    contact_id: Optional[uuid.UUID] = None
    note: Optional[str] = None
    discount: Optional[int] = Field(None, ge=0)

# --- Public Schemas ---

class TransactionPublic(BaseSchema):
    """Represents a transaction in public responses, without its items."""
    recorder_id: uuid.UUID
    contact_id: uuid.UUID
    note: Optional[str]
    status: TransactionStatus
    discount: int
    total_price: int
    
    # Nested public schemas for related objects
    # recorder: UserPublic
    # contact: ContactPublic

    class Config:
        from_attributes = True

class TransactionWithItemsPublic(TransactionPublic):
    """Extends TransactionPublic to include the list of associated items."""
    items: List[TransactionItemPublic] = []
