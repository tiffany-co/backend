from sqlalchemy import Column, String, Enum, Numeric
from app.models.base import BaseModel
from .enums.mesurement import MeasurementType
from .enums.transaction import TransactionType

class Item(BaseModel):
    """
    Represents an item template in the system.
    This model defines the default properties for categories of items
    that can be bought or sold in transactions.
    """
    __tablename__ = "item"

    name = Column(String, nullable=False, unique=True, index=True)
    category = Column(String, nullable=False, index=True)
    
    measurement_type = Column(Enum(MeasurementType), nullable=False)
    # The default transaction type can suggest if this item is typically bought or sold.
    transaction_type = Column(Enum(TransactionType), nullable=False)

    # Default financial properties. These are Numeric to handle decimal values accurately.
    karat_default = Column(Numeric(10, 2), nullable=True)
    ojrat_default = Column(Numeric(10, 2), nullable=True)
    profit_default = Column(Numeric(10, 2), nullable=True)
    tax_default = Column(Numeric(10, 2), nullable=True)

    def __repr__(self):
        return f"<Item(name='{self.name}', category='{self.category}')>"

