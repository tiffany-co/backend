import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base

class BaseModel(Base):
    """
    An abstract base model that provides common fields for all other models.
    This helps to avoid code duplication and ensures consistency.
    
    Fields:
    - id: A universally unique identifier (UUID) for the record.
    - created_at: The timestamp when the record was created.
    - updated_at: The timestamp when the record was last updated.
    """
    __abstract__ = True  # This tells SQLAlchemy not to create a table for this model.

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, server_default=func.now(), server_onupdate=func.now())
