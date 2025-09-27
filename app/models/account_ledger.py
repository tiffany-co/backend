from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class AccountLedger(BaseModel):
    """
    Represents an entry in the account ledger, tracking debts and payments for contacts.
    """
    __tablename__ = "account_ledger"

    contact_id = Column(ForeignKey("contact.id", ondelete="RESTRICT"), nullable=False, index=True)
    transaction_id = Column(ForeignKey("transaction.id", ondelete="SET NULL"), nullable=True, index=True)
    
    debt = Column(BigInteger, nullable=False, default=0, comment="Money that the shopkeeper owes to the customer (the reverse is not currently supported)")
    deadline = Column(DateTime, nullable=True, index=True)
    description = Column(Text, nullable=True)
    card_number = Column(String, nullable=True)
    bank_name = Column(String, nullable=True, index=True)

    # --- Relationships ---
    contact = relationship("Contact", back_populates="account_ledgers")
    transaction = relationship("Transaction", back_populates="account_ledger_entry")
    payments = relationship("Payment", back_populates="account_ledger")

    def __repr__(self):
        return f"<AccountLedger(id={self.id}, contact_id={self.contact_id}, debt='{self.debt}')>"
