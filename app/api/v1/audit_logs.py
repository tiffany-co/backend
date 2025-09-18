from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import uuid
from typing import List, Optional

from app.api import deps
from app.models.user import User, UserRole
from app.models.enums.audit_log import OperationType
from app.schema.audit_log import AuditLogPublic
from app.schema.error import ErrorDetail
from app.repository.audit_log import audit_log_repo

router = APIRouter()

@router.get(
    "/",
    response_model=List[AuditLogPublic],
    summary="[Admin] Search Audit Logs",
    description="Allows an administrator to search and filter the audit log to track changes.",
    responses={
        200: {"description": "A list of audit log entries matching the criteria."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
        403: {"model": ErrorDetail, "description": "Forbidden"},
    }
)
def search_audit_logs(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
    user_id: Optional[uuid.UUID] = Query(None, description="Filter by the user who performed the action."),
    operation: Optional[OperationType] = Query(None, description="Filter by the type of operation."),
    table_name: Optional[str] = Query(None, description="Filter by the name of the table that was affected (case-insensitive, partial match)."),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
):
    """
    Admin-only endpoint to search and paginate through the audit log.
    """
    logs = audit_log_repo.search(
        db, 
        user_id=user_id, 
        operation=operation, 
        table_name=table_name, 
        skip=skip, 
        limit=limit
    )
    return logs

