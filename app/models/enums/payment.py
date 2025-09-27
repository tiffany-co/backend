from enum import Enum

class PaymentMethod(str, Enum):
    """Enum for the method of payment."""
    CASH = "cash"
    CARD_TRANSACTION = "card_transaction"
    POS_MACHINE = "pos_machine"

class PaymentDirection(str, Enum):
    """
    Enum for the direction of a payment.
    - INCOMING: Money flowing into the business.
    - OUTGOING: Money flowing out of the business.
    - INTERNAL_TRANSFER: Funds moving between internal accounts (e.g., one contact's debt to another), with no net change to the business's cash balance.
    """
    INCOMING = "incoming"
    OUTGOING = "outgoing"
    INTERNAL_TRANSFER = "internal_transfer"