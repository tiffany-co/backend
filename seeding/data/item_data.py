from app.schema.item import ItemCreate
from app.schema.item_financial_profile import ItemFinancialProfileCreate
from app.models.enums.measurement import MeasurementType
from app.models.enums.transaction import TransactionType
from app.models.enums.item_type import ItemType

# This file now defines a more complex structure for seeding.
# Each item is a dictionary containing the main item data and a list of its financial profiles.

_zero_item_financial_profiles = [
    ItemFinancialProfileCreate(
        transaction_type=TransactionType.SELL,
        ojrat_default=0.0,
        profit_default=0.0,
        tax_default=0.0,
    ),
    ItemFinancialProfileCreate(
        transaction_type=TransactionType.BUY,
        ojrat_default=0.0,
        profit_default=0.0,
        tax_default=0.0,
    )
]

PREDEFINED_ITEMS_WITH_PROFILES = [
    {
        "item": ItemCreate(
            name=ItemType.NEW_GOLD,
            name_fa="طلای نو",
            category="طلا",
            description="جواهرات طلای ساخته شده استفاده نشده",
            measurement_type=MeasurementType.UNCOUNTABLE,
        ),
        "profiles": [
            ItemFinancialProfileCreate(
                transaction_type=TransactionType.SELL,
                ojrat_default=10.0,
                profit_default=6.0,
                tax_default=9.0,
            ),
            ItemFinancialProfileCreate(transaction_type=TransactionType.BUY)
        ]
    },
    {
        "item": ItemCreate(
            name=ItemType.USED_GOLD,
            name_fa="طلای مستعمل",
            category="طلا",
            description="جواهرات طلای استفاده شده",
            measurement_type=MeasurementType.UNCOUNTABLE,
        ),
        "profiles": [
            ItemFinancialProfileCreate(
                transaction_type=TransactionType.SELL,
                ojrat_default=0.0,
                profit_default=6.0,
                tax_default=9.0,
            ),
            ItemFinancialProfileCreate(
                transaction_type=TransactionType.BUY,
                ojrat_default=0.0,
                profit_default=0.0,
                tax_default=0.0,
            )
        ]
    },
    {
        "item": ItemCreate(
            name=ItemType.PERSIAN_COIN,
            name_fa="سکه پارسیان",
            category="سکه",
            description="سکه پارسیان، وزنی",
            measurement_type=MeasurementType.UNCOUNTABLE,
        ),
        "profiles": [
            ItemFinancialProfileCreate(
                transaction_type=TransactionType.SELL,
                ojrat_default=0.0,
                profit_default=5.0,
                tax_default=0.0,
            ),
            ItemFinancialProfileCreate(
                transaction_type=TransactionType.BUY,
                ojrat_default=0.0,
                profit_default=0.0,
                tax_default=0.0,
            )
        ]
    },
    {
        "item": ItemCreate(
            name=ItemType.MOLTEN_GOLD,
            name_fa="طلای آبشده",
            category="طلا",
            description="طلای آبشده گرفته شده در آزمایشگاه",
            measurement_type=MeasurementType.UNCOUNTABLE,
        ),
        "profiles": _zero_item_financial_profiles
    },
    {
        "item": ItemCreate(
            name=ItemType.SAFFRON,
            name_fa="زعفران",
            category="غیره",
            description="زعفران گرمی",
            measurement_type=MeasurementType.UNCOUNTABLE,
        ),
        "profiles": _zero_item_financial_profiles
    },
    {
        "item": ItemCreate(
            name=ItemType.EMAMI_COIN_86,
            name_fa="سکه امامی ۸۶",
            category="سکه",
            description="سکه تمام (امامی) ضرب ۸۶",
            measurement_type=MeasurementType.COUNTABLE,
        ),
        "profiles": _zero_item_financial_profiles
    },
    {
        "item": ItemCreate(
            name=ItemType.HALF_COIN_86,
            name_fa="نیم سکه ۸۶",
            category="سکه",
            description="نیم سکه ضرب ۸۶",
            measurement_type=MeasurementType.COUNTABLE,
        ),
        "profiles": _zero_item_financial_profiles
    },
    {
        "item": ItemCreate(
            name=ItemType.QUARTER_COIN_86,
            name_fa="ربع سکه ۸۶",
            category="سکه",
            description="ربع سکه ضرب ۸۶",
            measurement_type=MeasurementType.COUNTABLE,
        ),
        "profiles": _zero_item_financial_profiles
    },
    {
        "item": ItemCreate(
            name=ItemType.EMAMI_COIN_ETC,
            name_fa="سکه امامی غیره",
            category="سکه",
            description="سکه امامی ضرب نشده در ۸۶",
            measurement_type=MeasurementType.COUNTABLE,
        ),
        "profiles": _zero_item_financial_profiles
    },
    {
        "item": ItemCreate(
            name=ItemType.HALF_COIN_ETC,
            name_fa="نیم سکه غیره",
            category="سکه",
            description="نیم سکه ضرب نشده در ۸۶",
            measurement_type=MeasurementType.COUNTABLE,
        ),
        "profiles": _zero_item_financial_profiles
    },
    {
        "item": ItemCreate(
            name=ItemType.QUARTER_COIN_ETC,
            name_fa="ربع سکه غیره",
            category="سکه",
            description="ربع سکه ضرب نشده در ۸۶",
            measurement_type=MeasurementType.COUNTABLE,
        ),
        "profiles": _zero_item_financial_profiles
    },
    {
        "item": ItemCreate(
            name=ItemType.DOLLAR,
            name_fa="دلار",
            category="ارز",
            description="دلار آمریکا",
            measurement_type=MeasurementType.COUNTABLE,
        ),
        "profiles": _zero_item_financial_profiles
    },
    {
        "item": ItemCreate(
            name=ItemType.EURO,
            name_fa="یورو",
            category="ارز",
            description="یوروی اروپا",
            measurement_type=MeasurementType.COUNTABLE,
        ),
        "profiles": _zero_item_financial_profiles
    },
    {
        "item": ItemCreate(
            name=ItemType.POUND,
            name_fa="پوند",
            category="ارز",
            description="پوند انگلیس",
            measurement_type=MeasurementType.COUNTABLE,
        ),
        "profiles": _zero_item_financial_profiles
    },
]

