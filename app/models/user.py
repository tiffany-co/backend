from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.enums.user import UserRole
from app.models.permission import user_permission_association

class User(BaseModel):
    """
    Represents a user in the system.
    This model maps to the 'user' table in the database.
    """
    __tablename__ = "user"

    full_name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    
    # Bidirectional relationship with Contact
    contacts = relationship("Contact", back_populates="creator", cascade="all, delete-orphan")

    # Many-to-Many relationship with Permission
    permissions = relationship(
        "Permission",
        secondary=user_permission_association,
        back_populates="users"
    )

    def __repr__(self):
        """
        Provides a developer-friendly string representation of the User object.
        """
        return f"<User(id={self.id}, username='{self.username}', role='{self.role.value}')>"

