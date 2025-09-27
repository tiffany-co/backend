from enum import Enum

class ApprovalStatus(str, Enum):
    """
    A shared enum for the approval status of financial records like Transactions and Payments.
    """
    DRAFT = "draft"
    APPROVED_BY_USER = "approved_by_user"
    APPROVED_BY_ADMIN = "approved_by_admin"
