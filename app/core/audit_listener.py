import json
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import event, inspect
from sqlalchemy.orm import Session, object_session
from sqlalchemy.orm.attributes import get_history

from app.models.audit_log import AuditLog
from app.models.enums.audit_log import OperationType

def json_serializer(obj):
    """Custom JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime)):
        return obj.isoformat()
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, Decimal):
        return str(obj)
    if hasattr(obj, '__str__'):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

def get_obj_state(obj):
    """Converts a SQLAlchemy model instance into a JSON-serializable dictionary."""
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

@event.listens_for(Session, "before_flush")
def before_flush_listener(session, flush_context, instances):
    """
    Listen for session flush events.
    - Captures new objects to be processed after the flush.
    - Creates audit logs for updated and deleted objects.
    """
    user_id = session.info.get('current_user_id')
    if not user_id:
        return # for e.g. created in startup
    
    # Store new objects in the session's info dictionary to process them after the flush,
    # once their database-generated defaults (like ID) are populated.
    session.info.setdefault('audit_log_new_objects', []).extend(
        [obj for obj in session.new if not isinstance(obj, AuditLog)]
    )

    # Process updated (dirty) and deleted objects before the flush
    for obj in session.dirty:
        if isinstance(obj, AuditLog):
            continue
        
        obj_session = object_session(obj)
        if not obj_session:
            continue

        before_state = {}
        after_state = {}
        
        pk_dict = {pk.name: getattr(obj, pk.name) for pk in inspect(obj).mapper.primary_key}
        before_state.update(pk_dict)
        after_state.update(pk_dict)
        
        changes_found = False
        for attr in inspect(obj).attrs:
            history = get_history(obj, attr.key)
            if history.has_changes():
                changes_found = True
                before_state[attr.key] = history.deleted[0] if history.deleted else None
                after_state[attr.key] = history.added[0] if history.added else None
        
        if changes_found:
            session.add(AuditLog(
                user_id=user_id,
                operation=OperationType.UPDATE,
                table_name=obj.__tablename__,
                before_state=json.loads(json.dumps(before_state, default=json_serializer)),
                after_state=json.loads(json.dumps(after_state, default=json_serializer)),
            ))

    for obj in session.deleted:
        if isinstance(obj, AuditLog):
            continue
        session.add(AuditLog(
            user_id=user_id,
            operation=OperationType.DELETE,
            table_name=obj.__tablename__,
            before_state=json.loads(json.dumps(get_obj_state(obj), default=json_serializer))
        ))

@event.listens_for(Session, "after_flush")
def after_flush_listener(session, flush_context):
    """
    Listen for after-flush events to create audit logs for new objects.
    At this stage, database-generated values like IDs are available.
    """
    user_id = session.info.get('current_user_id')
    
    if not user_id:
        return # for e.g. created in startup
    
    new_objects = session.info.get('audit_log_new_objects', [])

    for obj in new_objects:
        # Now that the flush is complete, the object has its ID and other DB defaults.
        session.add(AuditLog(
            user_id=user_id,
            operation=OperationType.CREATE,
            table_name=obj.__tablename__,
            after_state=json.loads(json.dumps(get_obj_state(obj), default=json_serializer))
        ))
    
    # Clear the list from session.info to prevent reprocessing in nested flushes.
    session.info['audit_log_new_objects'] = []

