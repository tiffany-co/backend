from enum import Enum

class InvestorStatus(str, Enum):
    """
    Enum for the business status of an investor's account.
    """
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CLOSED = "closed"
