from sqlalchemy import Column, Enum, String, ForeignKey, BigInteger, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import BaseModel
from .enums.transaction import TransactionType

class TransactionItem(BaseModel):
    """
    Represents a single item within a larger transaction.
    """
    __tablename__ = "transaction_item"

    transaction_id = Column(UUID(as_uuid=True), ForeignKey("transaction.id", ondelete="CASCADE"), nullable=False, index=True)
    item_id = Column(UUID(as_uuid=True), ForeignKey("item.id"), nullable=False, index=True)
    
    transaction_type = Column(Enum(TransactionType, native_enum=False), nullable=False)
    title = Column(String, nullable=False, index=True)
    
    # Based on the inventory table, Numeric is the most flexible type to handle both weights (decimal) and counts (integer).
    weight_count = Column(Numeric(12, 2), nullable=False)
    
    unit_price = Column(BigInteger, nullable=False, default=0)
    total_price = Column(BigInteger, nullable=False, default=0)

    # Financial details for the item at the time of transaction
    karat = Column(Numeric(10, 2), nullable=True)
    ojrat = Column(Numeric(10, 2), nullable=True)
    profit = Column(Numeric(10, 2), nullable=True)
    tax = Column(Numeric(10, 2), nullable=True)
    
    # Relationships
    transaction = relationship("Transaction", back_populates="items")
    item = relationship("Item")
    
    def __repr__(self):
        return f"<TransactionItem(id={self.id}, title='{self.title}')>"
