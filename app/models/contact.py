from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
from app.models.enums.contact import ContactType

class Contact(BaseModel):
    """
    Represents a contact in the system (e.g., customer, supplier).
    This model maps to the 'contact' table in the database.
    """
    __tablename__ = "contact"

    first_name = Column(String, index=True, nullable=True)
    last_name = Column(String, index=True, nullable=False)
    national_number = Column(String, unique=True, index=True, nullable=True)
    phone_number = Column(String, unique=True, index=True, nullable=True)
    type = Column(Enum(ContactType), nullable=False, index=True)

    # Foreign key to link a contact to the user who created it.
    creator_user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    # SQLAlchemy relationship to easily access the creator user object from a contact object.
    creator = relationship("User", back_populates="contacts")
    transactions = relationship("Transaction", back_populates="contact")
    account_ledgers = relationship("AccountLedger", back_populates="contact", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="contact")

    def __repr__(self):
        """
        Provides a developer-friendly string representation of the Contact object.
        """
        return f"<Contact(id={self.id}, name='{self.first_name} {self.last_name}', type='{self.type.value}')>"
