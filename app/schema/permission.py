from pydantic import BaseModel, Field
from app.models.enums.permission import PermissionName
import uuid

class PermissionPublic(BaseModel):
    """
    Schema for public representation of a permission.
    Inherits id, created_at, and updated_at from BaseSchema.
    """
    id: uuid.UUID
    name: PermissionName

    class Config:
        from_attributes = True

class UserPermissionCreate(BaseModel):
    """
    Schema for adding a permission to a user.
    """
    permission_name: PermissionName = Field(..., example=PermissionName.CONTACT_UPDATE_ALL)

