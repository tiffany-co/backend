from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Investment(BaseModel):
    """
    Represents a single investment made by an investor.
    """
    __tablename__ = "investment"

    amount = Column(BigInteger, nullable=False, default=0, comment="The investment amount in Iranian Rials.")
    investor_id = Column(ForeignKey("investor.id"), nullable=False, index=True)

    # Link to the payment that generated this investment, if any.
    # `unique=True` enforces that a payment can only be linked to one investment.
    payment_id = Column(ForeignKey("payment.id", ondelete="SET NULL"), nullable=True, unique=True, index=True)

    # --- Relationships ---
    investor = relationship("Investor", back_populates="investments")
    payment = relationship("Payment", back_populates="investment_created")
    
    def __repr__(self):
        return f"<Investment(id={self.id}, amount={self.amount})>"
