from enum import Enum

class OperationType(str, Enum):
    """
    Enum for the type of operation performed in an audit log entry.
    """
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
