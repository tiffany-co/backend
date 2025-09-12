from pydantic import BaseModel, Field
from typing import Optional
import uuid

from app.models.enums.permission import PermissionName

class PermissionPublic(BaseModel):
    """
    Schema for public representation of a permission.
    """
    id: uuid.UUID
    name: PermissionName
    name_fa: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class UserPermissionCreate(BaseModel):
    """
    Schema for adding a permission to a user.
    """
    permission_name: PermissionName = Field(..., example=PermissionName.CONTACT_UPDATE_ALL)

