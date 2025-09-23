from sqlalchemy import Column, BigInteger, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Inventory(BaseModel):
    """
    Represents a snapshot of the shop's inventory at a specific point in time.
    Each row is a complete balance sheet. The column names for item balances
    are explicitly defined here and MUST correspond to the values in the ItemType enum.
    """
    __tablename__ = "inventory"

    transaction_id = Column(ForeignKey("transaction.id", ondelete="SET NULL"), nullable=True)
    description = Column(Text, nullable=True, comment="Note for manual adjustments, or link to a transaction.")

    # --- Balances ---
    money_balance = Column(BigInteger, nullable=False, default=0, comment="Cash balance in Rials")

    # --- Uncountable (Weights) & Currencies ---
    # These are defined as Numeric to handle decimal values with precision.
    # The attribute names (e.g., 'new_gold') MUST match the ItemType enum values.
    new_gold = Column(Numeric(12, 2), nullable=False, default=0)
    used_gold = Column(Numeric(12, 2), nullable=False, default=0)
    persian_coin = Column(Numeric(12, 2), nullable=False, default=0)
    molten_gold = Column(Numeric(12, 2), nullable=False, default=0)
    saffron = Column(Numeric(12, 2), nullable=False, default=0)
    dollar = Column(Numeric(12, 2), nullable=False, default=0)
    euro = Column(Numeric(12, 2), nullable=False, default=0)
    pound = Column(Numeric(12, 2), nullable=False, default=0)
    
    # --- Countable (Quantities) ---
    # These are defined as BigInteger for whole numbers.
    emami_coin_86 = Column(BigInteger, nullable=False, default=0)
    half_coin_86 = Column(BigInteger, nullable=False, default=0)
    quarter_coin_86 = Column(BigInteger, nullable=False, default=0)
    emami_coin_etc = Column(BigInteger, nullable=False, default=0)
    half_coin_etc = Column(BigInteger, nullable=False, default=0)
    quarter_coin_etc = Column(BigInteger, nullable=False, default=0)

    # Relationship
    transaction = relationship("Transaction", back_populates="inventory_entry")
