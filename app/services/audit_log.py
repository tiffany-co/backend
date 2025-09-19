from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from app.models.audit_log import AuditLog
from app.models.enums.audit_log import OperationType
from app.repository.audit_log import audit_log_repo

class AuditLogService:
    """
    Service layer for audit log business logic.
    Mainly for searching and retrieving logs, as creation is handled by the listener.
    """
    def search_logs(
        self,
        db: Session,
        *,
        user_id: Optional[uuid.UUID] = None,
        operation: Optional[OperationType] = None,
        table_name: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """Searches for audit logs using the repository."""
        return audit_log_repo.search(
            db,
            user_id=user_id,
            operation=operation,
            table_name=table_name,
            skip=skip,
            limit=limit
        )

audit_log_service = AuditLogService()
