from sqlalchemy import Column, BigInteger, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from .enums.shared import ApprovalStatus
from .enums.payment import PaymentMethod, PaymentDirection

class Payment(BaseModel):
    """
    Represents a single payment record, which can be incoming or outgoing.
    """
    __tablename__ = "payment"

    recorder_id = Column(ForeignKey("user.id"), nullable=False, index=True)
    amount = Column(BigInteger, nullable=False) 
    payment_method = Column(Enum(PaymentMethod, native_enum=False), nullable=False)
    direction = Column(Enum(PaymentDirection, native_enum=False), nullable=False)
    description = Column(Text, nullable=True)
    photo_holder_id = Column(ForeignKey("user.id"), nullable=True)
    status = Column(Enum(ApprovalStatus, native_enum=False), nullable=False, default=ApprovalStatus.DRAFT, index=True)

    # --- Mutually Exclusive Foreign Keys ---
    investor_id = Column(ForeignKey("investor.id", ondelete="SET NULL"), nullable=True, index=True)
    transaction_id = Column(ForeignKey("transaction.id", ondelete="SET NULL"), nullable=True, index=True)
    account_ledger_id = Column(ForeignKey("account_ledger.id", ondelete="SET NULL"), nullable=True, index=True)
    saved_bank_account_id = Column(ForeignKey("saved_bank_account.id", ondelete="SET NULL"), nullable=True, index=True)
    contact_id = Column(ForeignKey("contact.id", ondelete="RESTRICT"), nullable=True, index=True)

    # --- Relationships ---
    recorder = relationship("User", foreign_keys=[recorder_id])
    photo_holder = relationship("User", foreign_keys=[photo_holder_id])
    
    investment = relationship("Investment")
    transaction = relationship("Transaction", back_populates="payments")
    account_ledger = relationship("AccountLedger", back_populates="payments")
    saved_bank_account = relationship("SavedBankAccount", back_populates="payments")
    contact = relationship("Contact", back_populates="payments")
