from enum import Enum

class PaymentMethod(str, Enum):
    """Enum for the method of payment."""
    CASH = "cash"
    CARD_TRANSACTION = "card_transaction"
    POS_MACHINE = "pos_machine"

class PaymentDirection(str, Enum):
    """Enum for the direction of payment flow."""
    INCOMING = "incoming"
    OUTGOING = "outgoing"
