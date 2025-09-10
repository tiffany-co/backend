from enum import Enum

class PermissionName(str, Enum):
    """
    Enum for user permissions.
    The values are the string representations that will be stored in the database.
    """
    CONTACT_UPDATE_ALL = "contact_update_all"
