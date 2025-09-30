import uuid
from datetime import datetime
from decimal import Decimal

def json_serializer(obj):
    """
    Custom JSON serializer for objects not serializable by default,
    handling datetimes, UUIDs, Decimals, and Enums.
    """
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
