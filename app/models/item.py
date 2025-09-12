from sqlalchemy import Column, String, Enum, Numeric, Text, Boolean
from app.models.base import BaseModel
from .enums.measurement import MeasurementType
from .enums.transaction import TransactionType
from .enums.inventory_columns import InventoryColumnName

class Item(BaseModel):
    """
    Represents an item template in the system.
    """
    __tablename__ = "item"

    name = Column(String, nullable=False, unique=True, index=True)
    category = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    inventory_column_name = Column(Enum(InventoryColumnName, native_enum=False), nullable=False, unique=True)
    display_name_fa = Column(String, nullable=False, unique=True)

    measurement_type = Column(Enum(MeasurementType, native_enum=False), nullable=False)
    transaction_type = Column(Enum(TransactionType, native_enum=False), nullable=False)

    karat_default = Column(Numeric(10, 2), nullable=True)
    ojrat_default = Column(Numeric(10, 2), nullable=True)
    profit_default = Column(Numeric(10, 2), nullable=True)
    tax_default = Column(Numeric(10, 2), nullable=True)

    def __repr__(self):
        return f"<Item(name='{self.name}')>"

