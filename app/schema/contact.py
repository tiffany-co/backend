from pydantic import BaseModel, Field
import uuid
from typing import Optional

from .base import BaseSchema
from ..models.enums.contact import ContactType

# --- Base and Public Schemas ---

class ContactBase(BaseModel):
    """
    Base schema for contact data, containing common fields.
    """
    first_name: Optional[str] = Field(None, min_length=1, max_length=50, example="John")
    last_name: str = Field(..., min_length=1, max_length=50, example="Doe")
    national_number: Optional[str] = Field(None, min_length=10, max_length=10, example="1234567890")
    phone_number: Optional[str] = Field(None, min_length=10, max_length=15, example="09123456789")
    type: ContactType = Field(..., example=ContactType.CUSTOMER)

class ContactPublic(ContactBase, BaseSchema):
    """
    Schema for publicly available contact information.
    Includes the ID of the user who created the contact.
    """
    creator_user_id: uuid.UUID

    class Config:
        from_attributes = True

# --- Schemas for Creating and Updating ---

class ContactCreate(ContactBase):
    """
    Schema for creating a new contact.
    All fields from ContactBase are required.
    """
    pass

class ContactUpdate(BaseModel):
    """
    Schema for updating an existing contact. All fields are optional.
    """
    first_name: Optional[str] = Field(None, min_length=1, max_length=50, example="Jonathan")
    last_name: Optional[str] = Field(None, min_length=1, max_length=50, example="Doe")
    national_number: Optional[str] = Field(None, min_length=10, max_length=10, example="0987654321")
    phone_number: Optional[str] = Field(None, min_length=10, max_length=15, example="09123456789")
    type: Optional[ContactType] = Field(None, example=ContactType.SUPPLIER)
