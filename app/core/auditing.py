from contextvars import ContextVar
from typing import Dict, Any
from sqlalchemy import event
from sqlalchemy.orm import Session, sessionmaker

from app.models.user import User
from app.models.audit_log import AuditLog, OperationType
from fastapi.encoders import jsonable_encoder

# --- Context Variable ---
# This is a thread-safe way to store the current user for the duration of a request.
# The dependency in deps.py will set this, and the SQLAlchemy event listener will read it.
current_user_var: ContextVar[User | None] = ContextVar("current_user", default=None)

def get_state(obj):
    """Extracts the state of a SQLAlchemy model instance as a dictionary."""
    return {c.key: getattr(obj, c.key) for c in obj.__table__.columns}

@event.listens_for(sessionmaker, "after_flush")
def receive_after_flush(session: Session, flush_context):
    """
    This event listener is called after a database flush (before the commit).
    It inspects the session to find all new, updated, and deleted objects
    and creates an audit log entry for each one.
    """
    current_user = current_user_var.get()
    if not current_user:
        return # Do not log if there is no user in context (e.g., for scripts)

    # --- Process New Objects (CREATE) ---
    for obj in session.new:
        if isinstance(obj, AuditLog):
            continue # Don't log the creation of log entries themselves
        
        session.add(AuditLog(
            user_id=current_user.id,
            operation=OperationType.CREATE,
            table_name=obj.__tablename__,
            after_state=jsonable_encoder(get_state(obj))
        ))

    # --- Process Updated Objects (UPDATE) ---
    for obj in session.dirty:
        if isinstance(obj, AuditLog):
            continue
        
        # The 'committed_state' has the values from before the update
        before_state = {key: value for key, value in obj.__dict__.items() if not key.startswith('_')}
        
        session.add(AuditLog(
            user_id=current_user.id,
            operation=OperationType.UPDATE,
            table_name=obj.__tablename__,
            before_state=jsonable_encoder(before_state),
            after_state=jsonable_encoder(get_state(obj))
        ))
        
    # --- Process Deleted Objects (DELETE) ---
    for obj in session.deleted:
        if isinstance(obj, AuditLog):
            continue
            
        session.add(AuditLog(
            user_id=current_user.id,
            operation=OperationType.DELETE,
            table_name=obj.__tablename__,
            before_state=jsonable_encoder(get_state(obj))
        ))

