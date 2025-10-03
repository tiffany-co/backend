import uuid
from datetime import datetime
from decimal import Decimal
from app.models.base import BaseModel as SQLAlchemyBaseModel

def json_serializer(obj):
    """
    Custom JSON serializer for objects not serializable by default,
    handling datetimes, UUIDs, Decimals, and Enums.
    """
    # This check is specifically for the audit listener, which processes
    # live SQLAlchemy objects from relationships. It is not the cause of the
    # backup issue, as the backup service serializes database columns directly.
    if isinstance(obj, SQLAlchemyBaseModel):
        return str(obj.id)
    if isinstance(obj, (datetime)):
        return obj.isoformat()
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, Decimal):
        return str(obj)
    # This handles Enum members by getting their value
    if hasattr(obj, 'value'):
        return obj.value
    raise TypeError(f"Type {type(obj)} not serializable")
