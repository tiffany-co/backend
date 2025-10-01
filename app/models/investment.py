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

    # --- Relationships ---
    investor = relationship("Investor", back_populates="investments")

    def __repr__(self):
        return f"<Investment(id={self.id}, amount={self.amount})>"
