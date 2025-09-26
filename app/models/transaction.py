from sqlalchemy import Column, Enum, String, ForeignKey, Text, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import BaseModel
from .enums.transaction import TransactionStatus

class Transaction(BaseModel):
    """
    Represents a transaction, which is a collection of individual buy/sell items.
    """
    __tablename__ = "transaction"

    recorder_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, index=True)
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contact.id"), nullable=False, index=True)
    
    note = Column(Text, nullable=True)
    status = Column(Enum(TransactionStatus, native_enum=False), nullable=False, default=TransactionStatus.DRAFT, index=True)
    
    discount = Column(BigInteger, nullable=False, default=0)
    total_price = Column(BigInteger, nullable=False, default=0)

    # Relationships
    recorder = relationship("User")
    contact = relationship("Contact")
    items = relationship("TransactionItem", back_populates="transaction", cascade="all, delete-orphan")
    inventory_entry = relationship("Inventory", back_populates="transaction", uselist=False)
    account_ledger_entry = relationship("AccountLedger", back_populates="transaction", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Transaction(id={self.id}, status='{self.status.value}')>"
