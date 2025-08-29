from sqlalchemy import Column, String, Boolean, Enum, BigInteger
from app.models.base import BaseModel
from app.models.enums.item import ItemType

class Item(BaseModel):
    """
    Represents an item or product in the gold shop.
    This model maps to the 'item' table.
    """
    __tablename__ = "item"

    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    type = Column(Enum(ItemType), nullable=False, default=ItemType.UNCOUNTABLE)
    
    # Default values for transactions, stored as integers.
    karat_default = Column(BigInteger, nullable=False, default=750)
    ojrat_default = Column(BigInteger, nullable=False, default=0)
    profit_default = Column(BigInteger, nullable=False, default=0)
    tax_default = Column(BigInteger, nullable=False, default=0)

    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name}', type='{self.type.value}')>"
