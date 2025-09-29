from enum import Enum

class ItemType(str, Enum):
    """
    Enum for the specific types of items that correspond to columns in the Inventory table.
    This acts as the single source of truth for all inventory assets.
    """
    # Uncountable (Weights)
    NEW_GOLD = "new_gold"
    USED_GOLD = "used_gold"
    PERSIAN_COIN = "persian_coin"
    MOLTEN_GOLD = "molten_gold"
    SAFFRON = "saffron"
    
    # Countable (Quantities)
    EMAMI_COIN_403 = "emami_coin_403"
    HALF_COIN_403 = "half_coin_403"
    QUARTER_COIN_403 = "quarter_coin_403"
    EMAMI_COIN_86 = "emami_coin_86"
    HALF_COIN_86 = "half_coin_86"
    QUARTER_COIN_86 = "quarter_coin_86"
    EMAMI_COIN_ETC = "emami_coin_etc"
    HALF_COIN_ETC = "half_coin_etc"
    QUARTER_COIN_ETC = "quarter_coin_etc"
    ONE_GRAM_COIN = "one_gram_coin"
    
    # Currencies (Decimal)
    DOLLAR = "dollar"
    EURO = "euro"
    POUND = "pound"

