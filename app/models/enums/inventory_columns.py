from enum import Enum

class InventoryColumnName(str, Enum):
    """
    Enum for the column names in the Inventory table.
    This acts as a single source of truth to prevent typos and ensure consistency
    between the Item templates and the Inventory model.
    """
    NEW_GOLD_JEWELRY_WEIGHT = "new_gold_jewelry_weight"
    USED_GOLD_WEIGHT = "used_gold_weight"
    SILVER_BAR_WEIGHT = "silver_bar_weight"
    GOLD_COIN_COUNT = "gold_coin_count"
