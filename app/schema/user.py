import uuid
from pydantic import BaseModel, Field, field_serializer
from app.models.enums.user import UserRole
from typing import List, Optional, Any

from app.models.permission import Permission # Import the DB model for the serializer
from .permission import PermissionPublic

# --- Base Schemas ---

class UserBase(BaseModel):
    """
    Base schema for user data, containing common fields.
    """
    full_name: Optional[str] = Field(..., min_length=3, max_length=100, example="John Doe")
    username: str = Field(..., min_length=3, max_length=50, example="johndoe")
    phone_number: Optional[str] = Field(..., min_length=10, max_length=15, example="1234567890")
    is_active: bool = Field(default=True, example=True)

# --- Schemas for Creating Users ---

class UserCreate(UserBase):
    """
    Schema for creating a new user. Inherits from UserBase and adds the password.
    The 'role' is intentionally omitted, as it will be set to 'USER' by default in the service layer.
    """
    password: str = Field(..., min_length=8, example="a_strong_password")
    phone_number: str = Field(..., min_length=10, max_length=15, example="1234567890")
    password: str = Field(..., min_length=8, example="a_strong_password")
    
# --- Schemas for Creating Admins (just used in create admin script) ---
class AdminCreate(UserBase):
    """
    Schema specifically for the create_admin script.
    Inherits optional full_name and phone_number from UserBase
    """
    password: str = Field(..., example="a_strong_password", description="For convenience, we also included the ability to set a weak username for the admin.")
    role: UserRole = Field(..., example=UserRole.ADMIN)

# --- Schemas for Updating Users ---
class UserUpdateMe(BaseModel):
    """
    Schema for a user updating their own profile.
    'is_active' is intentionally omitted to prevent users from deactivating themselves.
    """
    username: Optional[str] = Field(None, min_length=3, max_length=50, example="new_johndoe")
    full_name: Optional[str] = Field(None, min_length=3, max_length=100, example="Johnathan Doe")
    phone_number: Optional[str] = Field(None, min_length=10, max_length=15, example="0987654321")
    password: Optional[str] = Field(None, min_length=8, example="a_new_strong_password")

class UserUpdateAdmin(UserUpdateMe):
    """
    Schema for an admin updating any user's profile.
    Includes the ability to change the 'is_active' status.
    """
    password: Optional[str] = Field(None, min_length=4, example="a_new_strong_password")
    is_active: Optional[bool] = Field(None, example=True)

# --- Schemas for Public Responses ---

class UserPublic(UserBase):
    """
    Schema for representing a user in public API responses.
    Excludes sensitive data like the password.
    """
    id: uuid.UUID = Field(..., example=uuid.uuid4())
    role: UserRole = Field(..., example=UserRole.USER)
    permissions: List[PermissionPublic] = []

    class Config:
        from_attributes = True

class UserInList(UserBase):
    """
    A specialized public schema for user lists.
    It includes a minimal representation of permissions (name only).
    """
    id: uuid.UUID = Field(..., example=uuid.uuid4())
    role: UserRole
    permissions: List[PermissionPublic] = []
    
    @field_serializer('permissions')
    def serialize_permissions(self, perms: List[Permission]) -> List[str]:
        """
        This function is called by Pydantic before sending the response.
        It converts the list of Permission database objects into a simple list of their string names.
        """
        return [p.name.value for p in perms]

    class Config:
        from_attributes = True
