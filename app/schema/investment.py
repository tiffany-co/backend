import uuid
from .base import BaseSchema
from typing import Optional
from pydantic import ConfigDict

class InvestmentPublic(BaseSchema):
    """Public schema for representing an investment."""
    amount: int
    investor_id: uuid.UUID
    payment_id: Optional[uuid.UUID]
    
    model_config = ConfigDict(from_attributes=True)
