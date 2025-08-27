from pydantic import BaseModel, Field
from typing import Optional
import uuid
from app.models.enums.contact import ContactType
from .base import BaseSchema

# --- Contact Schemas ---

# Base properties for a contact.
class ContactBase(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: str = Field(..., max_length=50)
    national_number: Optional[str] = Field(None, min_length=10, max_length=10)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=15)
    type: ContactType

# Properties required to create a new contact.
class ContactCreate(ContactBase):
    pass # No extra fields needed beyond the base.

# Properties allowed for updating a contact. All fields are optional.
class ContactUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    national_number: Optional[str] = Field(None, min_length=10, max_length=10)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=15)
    type: Optional[ContactType] = None

# Public representation of a Contact, including the creator's ID.
class ContactPublic(BaseSchema, ContactBase):
    creator_user_id: uuid.UUID
