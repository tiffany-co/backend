from sqlalchemy.orm import Session
from typing import Any, Dict, Optional
from pydantic import BaseModel

from app.models.user import User
from app.models.base import BaseModel as DBModel
from app.models.enums.audit_log import OperationType
from app.repository.audit_log import audit_log_repo
from fastapi.encoders import jsonable_encoder

class AuditLogService:
    """
    A centralized service for creating audit log entries.
    This provides an abstract, DRY way to handle logging across all other services.
    """
    def create_log(
        self,
        db: Session,
        *,
        current_user: User,
        operation: OperationType,
        db_obj: DBModel, # The SQLAlchemy object that was changed
        obj_in: Optional[BaseModel | Dict[str, Any]] = None, # The Pydantic schema or dict with new data
    ):
        """
        Creates a structured audit log entry.
        """
        table_name = db_obj.__tablename__
        before_state = None
        after_state = None

        if operation == OperationType.CREATE:
            after_state = jsonable_encoder(db_obj)
        
        elif operation == OperationType.UPDATE:
            before_state = jsonable_encoder(db_obj)
            # Create a dictionary of the updated object
            after_state_obj = db_obj.__class__(**jsonable_encoder(db_obj))
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)
            
            for field in update_data:
                setattr(after_state_obj, field, update_data[field])

            after_state = jsonable_encoder(after_state_obj)

        elif operation == OperationType.DELETE:
            before_state = jsonable_encoder(db_obj)

        log_data = {
            "user_id": current_user.id,
            "operation": operation,
            "table_name": table_name,
            "before_state": before_state,
            "after_state": after_state,
        }
        audit_log_repo.create(db, obj_in=log_data)

audit_log_service = AuditLogService()
