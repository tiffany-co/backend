from enum import Enum

class TransactionType(str, Enum):
    """
    Enum for the type of a transaction line item.
    - BUY: The shop is acquiring the item.
    - SELL: The shop is selling the item.
    """
    BUY = "buy"
    SELL = "sell"
