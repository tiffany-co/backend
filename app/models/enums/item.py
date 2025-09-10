import enum

class ItemType(str, enum.Enum):
    """
    Enum for the type of an item.
    - Countable: Items that are sold by quantity (e.g., rings, necklaces).
    - Uncountable: Items sold by weight (e.g., gold bars, chains).
    """
    COUNTABLE = "countable"
    UNCOUNTABLE = "uncountable"
