import uuid
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from .base import BaseSchema
from ..models.enums.audit_log import OperationType

class AuditLogPublic(BaseSchema):
    """
    Schema for public representation of an audit log entry.
    """
    user_id: Optional[uuid.UUID]
    operation: OperationType
    table_name: str
    before_state: Optional[Dict[str, Any]]
    after_state: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True

