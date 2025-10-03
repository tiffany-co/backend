from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional

from .base import BaseSchema

class SavedBankAccountBase(BaseModel):
    """
    Base schema for saved bank account data.
    """
    name: str = Field(..., min_length=2, max_length=100, json_schema_extra={"example": "Main Business Account"})
    # --- UPDATED: description is now optional ---
    description: Optional[str] = Field(None, max_length=500, json_schema_extra={"example": "Primary account for daily transactions."})
    # --- NEW: Added card_number with validation ---
    card_number: Optional[str] = Field(None, min_length=16, max_length=16, json_schema_extra={"example": "1111222233334444"})

    @field_validator("card_number")
    def validate_card_number_is_digits(cls, v):
        """Ensures the card number contains only digits."""
        if v is not None and not v.isdigit():
            raise ValueError("Card number must contain only digits.")
        return v

class SavedBankAccountCreate(SavedBankAccountBase):
    """Schema for creating a new saved bank account."""
    pass

class SavedBankAccountUpdate(BaseModel):
    """
    Schema for updating a saved bank account. All fields are optional.
    """
    name: Optional[str] = Field(None, min_length=2, max_length=100, json_schema_extra={"example": "Updated Business Account"})
    description: Optional[str] = Field(None, max_length=500, json_schema_extra={"example": "Updated description."})
    card_number: Optional[str] = Field(None, min_length=16, max_length=16, json_schema_extra={"example": "5555666677778888"})

    @field_validator("card_number")
    def validate_card_number_is_digits(cls, v):
        """Ensures the card number contains only digits on update."""
        if v is not None and not v.isdigit():
            raise ValueError("Card number must contain only digits.")
        return v
        
class SavedBankAccountPublic(SavedBankAccountBase, BaseSchema):
    """
    Schema for publicly available saved bank account information.
    """
    model_config = ConfigDict(from_attributes=True)

