import uuid
from .base import BaseSchema
from typing import Optional

class InvestmentPublic(BaseSchema):
    """Public schema for representing an investment."""
    amount: int
    investor_id: uuid.UUID
    payment_id: Optional[uuid.UUID]
    
    class Config:
        from_attributes = True
