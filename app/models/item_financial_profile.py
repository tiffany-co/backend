from sqlalchemy import Column, Enum, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from .enums.transaction import TransactionType

class ItemFinancialProfile(BaseModel):
    """
    Represents the default financial rules for an Item under specific conditions
    (e.g., for buying vs. selling).
    """
    __tablename__ = "item_financial_profile"

    item_id = Column(ForeignKey("item.id"), nullable=False)
    transaction_type = Column(Enum(TransactionType, native_enum=False), nullable=False)

    karat_default = Column(Numeric(10, 2), nullable=True)
    ojrat_default = Column(Numeric(10, 2), nullable=True)
    profit_default = Column(Numeric(10, 2), nullable=True)
    tax_default = Column(Numeric(10, 2), nullable=True)

    # Relationship back to the parent Item
    item = relationship("Item", back_populates="financial_profiles")

    def __repr__(self):
        return f"<ItemFinancialProfile(item_id={self.item_id}, type='{self.transaction_type.value}')>"

