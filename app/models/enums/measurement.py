from enum import Enum

class MeasurementType(str, Enum):
    """
    Enum for how an item is measured.
    - COUNTABLE: Measured by quantity (e.g., coins, watches).
    - UNCOUNTABLE: Measured by weight (e.g., gold jewelry, silver bars).
    """
    COUNTABLE = "countable"
    UNCOUNTABLE = "uncountable"
