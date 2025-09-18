from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uuid

from .base import BaseSchema
from ..models.enums.audit_log import OperationType

class AuditLogPublic(BaseSchema):
    """
    Schema for public representation of an audit log entry.
    """
    user_id: Optional[uuid.UUID] = None
    operation: OperationType
    table_name: str
    before_state: Optional[Dict[str, Any]] = None
    after_state: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

