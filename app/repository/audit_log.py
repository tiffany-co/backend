from sqlalchemy.orm import Session
from typing import List, Optional, Any
import uuid

from app.repository.base import BaseRepository
from app.models.audit_log import AuditLog
from app.models.enums.audit_log import OperationType

class AuditLogRepository(BaseRepository[AuditLog, Any, Any]):
    """
    Repository for audit log related database operations.
    """
    def search(
        self,
        db: Session,
        *,
        user_id: Optional[uuid.UUID] = None,
        operation: Optional[OperationType] = None,
        table_name: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """
        Searches for audit logs based on a combination of criteria.
        """
        query = db.query(self.model)
        
        if user_id:
            query = query.filter(self.model.user_id == user_id)
        if operation:
            query = query.filter(self.model.operation == operation)
        if table_name:
            query = query.filter(self.model.table_name.ilike(f"%{table_name}%"))
            
        return query.order_by(self.model.created_at.desc()).offset(skip).limit(limit).all()

audit_log_repo = AuditLogRepository(AuditLog)
