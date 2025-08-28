import enum

class PermissionName(str, enum.Enum):
    """
    Enum for defining specific, granular permissions in the system.
    This makes the permission system extensible for the future.
    """
    # Contact Permissions
    CONTACT_READ_ALL = "contact_read_all"
    CONTACT_UPDATE_ALL = "contact_update_all"
    CONTACT_SEARCH = "contact_search"
    
    # User Permissions (for admin)
    USER_CREATE = "user_create"
    USER_READ_ALL = "user_read_all"
    USER_UPDATE = "user_update"
    USER_DELETE = "user_delete"
