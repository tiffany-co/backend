import uuid
from pydantic import BaseModel, Field
from typing import Optional

from .base import BaseSchema
from .contact import ContactPublic
from app.models.enums.investor import InvestorStatus

# --- Schemas for Admin Operations ---

class InvestorCreate(BaseModel):
    """Schema for an admin to create a new investor."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    national_number: Optional[str] = Field(None, min_length=10, max_length=10)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=15)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

class InvestorUpdate(BaseModel):
    """Schema for an admin to update an investor's status."""
    status: Optional[InvestorStatus] = None

class InvestorPublic(BaseSchema):
    """Public schema for representing an investor, including nested contact info."""
    credit: int
    status: InvestorStatus
    user_id: uuid.UUID
    contact_id: uuid.UUID
    contact: ContactPublic

    class Config:
        from_attributes = True

# --- Schemas for Investor's Own View ---

class InvestorProfilePublic(BaseSchema):
    """Schema for an investor viewing their own profile."""
    credit: int
    status: InvestorStatus
    contact: ContactPublic

    class Config:
        from_attributes = True

class InvestorPasswordUpdate(BaseModel):
    """Schema for an investor to update their own password."""
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)
