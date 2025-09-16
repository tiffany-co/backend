from sqlalchemy import Column, String, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from .enums.measurement import MeasurementType

class Item(BaseModel):
    """
    Represents the core identity of an inventory asset (the "What").
    Financial details are stored in the related ItemFinancialProfile model.
    """
    __tablename__ = "item"

    name = Column(String, nullable=False, unique=True, index=True) # This will be the ItemType enum value
    name_fa = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    measurement_type = Column(Enum(MeasurementType, native_enum=False), nullable=False)

    # One-to-many relationship with financial profiles
    financial_profiles = relationship(
        "ItemFinancialProfile", 
        back_populates="item", 
        cascade="all, delete-orphan",
        lazy="selectin" # Eagerly load profiles when an item is fetched
    )

    def __repr__(self):
        return f"<Item(name='{self.name}')>"
