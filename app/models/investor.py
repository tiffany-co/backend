from sqlalchemy import Column, BigInteger, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.enums.investor import InvestorStatus

class Investor(BaseModel):
    """
    Represents an investor profile, linking a User and a Contact to investment data.
    """
    __tablename__ = "investor"

    credit = Column(BigInteger, nullable=False, default=0, comment="The investor's withdrawable credit in Iranian Rials.")
    status = Column(Enum(InvestorStatus, native_enum=False), nullable=False, default=InvestorStatus.ACTIVE, index=True)

    user_id = Column(ForeignKey("user.id"), nullable=False, unique=True, index=True)
    contact_id = Column(ForeignKey("contact.id"), nullable=False, unique=True, index=True)

    # --- Relationships ---
    user = relationship("User", back_populates="investor_profile")
    contact = relationship("Contact", back_populates="investor_profile")
    investments = relationship("Investment", back_populates="investor", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="investor")

    def __repr__(self):
        return f"<Investor(id={self.id}, user_id={self.user_id}, status='{self.status.value}')>"
