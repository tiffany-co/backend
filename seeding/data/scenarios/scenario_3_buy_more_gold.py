from app.models.enums.shared import ApprovalStatus
from app.models.enums.payment import PaymentMethod, PaymentDirection
from app.models.enums.transaction import TransactionType

SCENARIO_3_BUY_MORE_GOLD = {
    "name": "Scenario 3: Buy Gold with Partial Payment",
    "recorder_username": "reza",
    "contact_national_number": "9876543210", # فرهاد احمدی
    "transaction": {
        "note": "خرید سکه یک گرمی از آقای احمدی",
        "discount": 0,
    },
    "items": [
        {
            "item_name": "one_gram_coin",
            "title": "سکه یک گرمی",
            "transaction_type": TransactionType.BUY,
            "weight_count": 10,
            "unit_price": 40_000_000,
        }
    ],
    "payments": [
        {
            "payment_method": PaymentMethod.CASH,
            "direction": PaymentDirection.OUTGOING,
            "description": "پرداخت نقدی قسمتی از مبلغ خرید سکه گرمی",
            "amount": 100_000_000,
        }
    ],
    "ledger": {
        "deadline": "2025-11-01T18:00:00",
        "description": "بدهی جدید بابت خرید سکه گرمی",
    }
}
