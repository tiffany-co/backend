import uuid
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

from app.models.enums.shared import ApprovalStatus
from .base import BaseSchema
from .transaction_item import TransactionItemPublic

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
    status: ApprovalStatus
    discount: int
    total_price: int
    
    # Nested public schemas for related objects
    # recorder: UserPublic
    # contact: ContactPublic

    model_config = ConfigDict(from_attributes=True)

class TransactionWithItemsPublic(TransactionPublic):
    """Extends TransactionPublic to include the list of associated items."""
    items: List[TransactionItemPublic] = []
