import enum

class UserRole(str, enum.Enum):
    """
    Enum for user roles to ensure data consistency.
    Using an Enum is better than raw strings as it prevents typos
    and makes the code more readable and maintainable.
    """
    ADMIN = "admin"
    USER = "user"
    INVESTOR = "investor"
