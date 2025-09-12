from app.schema.item import ItemCreate
from app.models.enums.measurement import MeasurementType
from app.models.enums.transaction import TransactionType
from app.models.enums.inventory_columns import InventoryColumnName

# This file contains the raw data for items to be seeded into the database.
PREDEFINED_ITEMS = [
    ItemCreate(
        name="New Gold Jewelry",
        category="Jewelry",
        description="Category for selling new, manufactured gold jewelry.",
        inventory_column_name=InventoryColumnName.NEW_GOLD_JEWELRY_WEIGHT,
        display_name_fa="طلای نو (گرم)",
        measurement_type=MeasurementType.UNCOUNTABLE,
        transaction_type=TransactionType.SELL,
        ojrat_default=10.0,
        profit_default=7.0,
        tax_default=9.0,
        karat_default=750
    ),
    ItemCreate(
        name="Used Gold",
        category="Jewelry",
        description="Category for buying used or scrap gold from customers.",
        inventory_column_name=InventoryColumnName.USED_GOLD_WEIGHT,
        display_name_fa="طلای دست دوم (گرم)",
        measurement_type=MeasurementType.UNCOUNTABLE,
        transaction_type=TransactionType.BUY,
        ojrat_default=0.0,
        profit_default=2.0,
        tax_default=0.0,
        karat_default=750
    ),
    ItemCreate(
        name="Gold Coin",
        category="Coin",
        description="Category for buying or selling standard gold coins.",
        inventory_column_name=InventoryColumnName.GOLD_COIN_COUNT,
        display_name_fa="سکه طلا (عدد)",
        measurement_type=MeasurementType.COUNTABLE,
        transaction_type=TransactionType.SELL,
        ojrat_default=0.0,
        profit_default=2.5,
        tax_default=0.0,
        karat_default=900
    ),
    ItemCreate(
        name="Silver Bar",
        category="Bullion",
        description="Category for buying or selling pure silver bars.",
        inventory_column_name=InventoryColumnName.SILVER_BAR_WEIGHT,
        display_name_fa="شمش نقره (گرم)",
        measurement_type=MeasurementType.UNCOUNTABLE,
        transaction_type=TransactionType.BUY,
        ojrat_default=0.0,
        profit_default=5.0,
        tax_default=0.0,
        karat_default=999
    ),
]
