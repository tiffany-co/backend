from app.models.enums.transaction import TransactionType

SCENARIO_1_BUY_GOLD = {
    "name": "Scenario 1: Buy Gold & Create Debt",
    "recorder_username": "reza",
    "contact_national_number": "9876543210", # فرهاد احمدی
    "transaction": {
        "note": "خرید طلای دست دوم از آقای احمدی",
        "discount": 0,
    },
    "items": [
        {
            "item_name": "used_gold",
            "title": "النگو کارکرده",
            "transaction_type": TransactionType.BUY,
            "weight_count": 50.0,
            "unit_price": 90_000_000,
        }
    ],
    "ledger": {
        "deadline": "2025-10-20T18:00:00",
        "description": "بدهی بابت خرید طلا از آقای احمدی",
        # Debt is calculated automatically from transaction total
    }
}
