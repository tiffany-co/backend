from sqlalchemy import Column, Enum, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from .enums.audit_log import OperationType

class AuditLog(BaseModel):
    """
    Represents an entry in the audit log, tracking changes to the database.
    This table is populated automatically by SQLAlchemy event listeners.
    """
    __tablename__ = "audit_log"

    user_id = Column(ForeignKey("user.id"), nullable=True, index=True, comment="The user who performed the action. Can be null for system actions.")
    operation = Column(Enum(OperationType, native_enum=False), nullable=False, index=True)
    table_name = Column(String, nullable=False, index=True)
    
    before_state = Column(JSONB, nullable=True, comment="The state of the record before the change (for UPDATE and DELETE).")
    after_state = Column(JSONB, nullable=True, comment="The state of the record after the change (for CREATE and UPDATE).")

    user = relationship("User", lazy="selectin")
