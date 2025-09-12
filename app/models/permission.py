from sqlalchemy import Column, Enum, Text, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.enums.permission import PermissionName
from .user import user_permission_association

class Permission(BaseModel):
    """
    Represents a specific permission in the system.
    """
    __tablename__ = "permission"

    name = Column(Enum(PermissionName, native_enum=False), nullable=False, unique=True, index=True)
    name_fa = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)

    users = relationship(
        "User",
        secondary=user_permission_association,
        back_populates="permissions"
    )
    
    def __repr__(self):
        return f"<Permission(name='{self.name.value}')>"

