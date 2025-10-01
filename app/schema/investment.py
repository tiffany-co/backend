import uuid
from .base import BaseSchema

class InvestmentPublic(BaseSchema):
    """Public schema for representing an investment."""
    amount: int
    investor_id: uuid.UUID
    
    class Config:
        from_attributes = True
