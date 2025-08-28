from sqlalchemy import Column, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base
from app.models.base import BaseModel
from app.models.enums.permission import PermissionName

# Association table for the many-to-many relationship between users and permissions.
user_permission_association = Table(
    "user_permission",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True),
    Column("permission_id", UUID(as_uuid=True), ForeignKey("permission.id"), primary_key=True),
)

class Permission(BaseModel):
    """
    Represents a specific permission in the system.
    This model maps to the 'permission' table.
    """
    __tablename__ = "permission"

    name = Column(Enum(PermissionName), nullable=False, unique=True, index=True)

    # The 'users' relationship will be available on Permission objects,
    # but it's defined via the 'back_populates' on the User model.
    
    def __repr__(self):
        return f"<Permission(name='{self.name.value}')>"
