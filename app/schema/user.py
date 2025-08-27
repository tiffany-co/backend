from pydantic import BaseModel, Field
from typing import Optional
from app.models.enums.user import UserRole
from .base import BaseSchema

# --- User Schemas ---

# Base properties shared by all user-related schemas.
class UserBase(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    phone_number: str = Field(..., min_length=10, max_length=15)
    role: UserRole = UserRole.USER
    is_active: Optional[bool] = True

# Properties required for creating a new user.
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

# Properties allowed for updating a user. All fields are optional.
class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=3, max_length=100)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=15)
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

# Public representation of a User, inherits from BaseSchema and UserBase.
# This schema is used for API responses to avoid exposing sensitive data.
class UserPublic(BaseSchema, UserBase):
    pass # Inherits all necessary fields, no additional fields needed.
