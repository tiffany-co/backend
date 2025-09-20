from enum import Enum

class TransactionType(str, Enum):
    """
    Enum for the type of a transaction line item.
    - BUY: The shop is acquiring the item.
    - SELL: The shop is selling the item.
    """
    BUY = "buy"
    SELL = "sell"

class TransactionStatus(str, Enum):
    """
    Enum for the status of a transaction.
    - DRAFT: The transaction is in progress and has not been finalized.
    - APPROVED_BY_USER: The transaction has been confirmed by a regular user.
    - APPROVED_BY_ADMIN: The transaction has been confirmed by an admin.
    """
    DRAFT = "draft"
    APPROVED_BY_USER = "approved_by_user"
    APPROVED_BY_ADMIN = "approved_by_admin"
