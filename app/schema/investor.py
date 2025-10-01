import uuid
from pydantic import BaseModel, Field, computed_field, ConfigDict
from typing import Optional, Any

from .base import BaseSchema
from .contact import ContactPublic
from app.models.enums.investor import InvestorStatus

# --- Schemas for Creating and Updating ---

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
    credit: Optional[int] = Field(None, ge=0, description="The new credit balance for the investor in Rials.")

class InvestorPasswordUpdate(BaseModel):
    """Schema for an investor to update their own password."""
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)

# --- Base Schema for Public Views ---

class InvestorSchema(BaseSchema):
    """A base schema for public investor data, applying DRY principles."""
    credit: int
    status: InvestorStatus
    contact: ContactPublic
    
    # This field allows Pydantic to access the 'user' relationship from the ORM model
    # but excludes it from the final JSON output, resolving the AttributeError.
    user: Any = Field(..., exclude=True)

    # Pydantic v2 configuration to enable ORM mode (replaces from_orm=True)
    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def username(self) -> str:
        """
        Dynamically computes the username from the related User object.
        This resolves the from_orm deprecation warning and uses the modern Pydantic v2 approach.
        Requires the 'user' relationship to be eagerly loaded on the ORM model.
        """
        return self.user.username

# --- Schemas for API Responses ---

class InvestorPublic(InvestorSchema):
    """
    Public schema for representing an investor, intended for admins and general lists.
    Includes the user_id for direct reference.
    """
    user_id: uuid.UUID

class InvestorProfilePublic(InvestorSchema):
    """
    Schema for an investor viewing their own profile.
    Inherits all fields from the base schema.
    """
    pass

