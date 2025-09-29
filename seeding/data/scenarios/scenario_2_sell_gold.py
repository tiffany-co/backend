from app.models.enums.shared import ApprovalStatus
from app.models.enums.payment import PaymentMethod, PaymentDirection
from app.models.enums.transaction import TransactionType

SCENARIO_2_SELL_GOLD = {
    "name": "Scenario 2: Sell Gold & Settle Debt",
    "recorder_username": "admin",
    "contact_national_number": "1234567891", # مریم رضایی
    "transaction": {
        "note": "فروش سکه به خانم رضایی",
        "discount": 1_000_000,
    },
    "items": [
        {
            "item_name": "emami_coin_403",
            "title": "سکه امامی ۱۴۰۳",
            "transaction_type": TransactionType.SELL,
            "weight_count": 2,
            "unit_price": 350_000_000,
            "profit_default": 2.0,
            "tax_default": 9.0,
        }
    ],
    "payments": [
        {
            "payment_method": PaymentMethod.CARD_TRANSACTION,
            "direction": PaymentDirection.INTERNAL_TRANSFER,
            "description": "انتقال طلب از خانم رضایی به حساب آقای احمدی",
            "amount_description": "SETTLE_PREVIOUS_DEBT",
            "settle_contact_national_number": "9876543210", # Settle Ahmadi's debt
        },
        { 
            "payment_method": PaymentMethod.CASH,
            "direction": PaymentDirection.OUTGOING,
            "description": "پرداخت مابقی طلب آقای احمدی",
            "amount_description": "REMAINDER_OF_PREVIOUS_DEBT",
            "settle_contact_national_number": "9876543210", # Settle Ahmadi's debt
            "saved_bank_account_name": "بانک ملت فروشگاه"
        }
    ]
}
