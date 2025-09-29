from app.models.enums.user import UserRole
from app.models.enums.contact import ContactType
from app.models.enums.shared import ApprovalStatus
from app.models.enums.payment import PaymentMethod, PaymentDirection
from app.models.enums.transaction import TransactionType
from app.schema.user import UserCreate, AdminCreate
from app.schema.contact import ContactCreate
from app.schema.saved_bank_account import SavedBankAccountCreate
from app.schema.inventory import InventoryAdjust, InventoryItemsSchema
from app.schema.transaction import TransactionCreate
from app.schema.account_ledger import AccountLedgerCreate
from app.schema.payment import PaymentCreate

# This file contains sample data for populating the database for a demo.

DEMO_USERS = [
    AdminCreate(
        full_name="حسین عجمی",
        username='admin',
        phone_number='09215256536',
        password='1111',
        role=UserRole.ADMIN
    ),
    UserCreate(
        full_name="رضا فراستی",
        username="reza",
        phone_number="09121112233",
        password="11111111",
    ),
]

DEMO_CONTACTS = [
    {
        "owner_username": "admin",
        "contact": ContactCreate(
            first_name="فرهاد",
            last_name="احمدی",
            phone_number="09151234567",
            national_number="9876543210", # This contact will have a positive balance with us
            type=ContactType.CUSTOMER,
        ),
    },
    {
        "owner_username": "reza",
        "contact": ContactCreate(
            first_name="مریم",
            last_name="رضایی",
            phone_number="09157654321",
            national_number="1234567891", # This contact will owe us money
            type=ContactType.CUSTOMER,
        ),
    },
]

DEMO_SAVED_BANK_ACCOUNTS = [
    SavedBankAccountCreate(
        name="بانک ملت فروشگاه",
        description="حساب اصلی فروشگاه",
        card_number="6104337811112222"
    ),
]

DEMO_INVENTORY = InventoryAdjust(
    description="موجودی اولیه فروشگاه",
    money_balance=15_000_000_000,
    inventory=InventoryItemsSchema(
        new_gold=500.0,
        used_gold=1250.75,
        emami_coin_403=20,
        one_gram_coin=100,
        dollar=5000.25
    )
)

# --- Scenarios ---

# Scenario 1: We buy gold from Customer Ahmadi and owe him money.
TRANSACTION_1_BUY_GOLD = {
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

# Scenario 2: Customer Rezai buys gold from us, creating a debt.
# We then settle her previous debt with an internal transfer and pay the rest.
TRANSACTION_2_SELL_GOLD = {
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
            "profit": 2.0,
            "tax": 9.0,
        }
    ],
    "payments": [
        {
            "payment_method": PaymentMethod.CARD_TRANSACTION,
            "direction": PaymentDirection.INTERNAL_TRANSFER,
            "description": "انتقال طلب از خانم رضایی به حساب آقای احمدی",
            "status": ApprovalStatus.APPROVED_BY_ADMIN,
            "contact_national_number": "9876543210", # From Ahmadi
        },
        { # Outgoing payment for the remaining amount
            "payment_method": PaymentMethod.CASH,
            "direction": PaymentDirection.OUTGOING,
            "description": "پرداخت مابقی طلب آقای احمدی",
            "status": ApprovalStatus.APPROVED_BY_ADMIN,
            "saved_bank_account_name":  "بانک ملت فروشگاه"
        }
    ]
}


# Scenario 3: We buy more gold from Customer Ahmadi.
# We pay some in cash and the rest becomes a new debt for us.
TRANSACTION_3_BUY_MORE_GOLD = {
    "recorder_username": "reza",
    "contact_national_id": "9876543210", # فرهاد احمدی
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
            "profit": 1.0,
        }
    ],
    "ledger": {
        "deadline": "2025-11-01T18:00:00",
        "description": "بدهی جدید بابت خرید سکه گرمی",
    },
    "payment": {
        "payment_method": PaymentMethod.CASH,
        "direction": PaymentDirection.OUTGOING,
        "description": "پرداخت نقدی قسمتی از مبلغ خرید سکه گرمی",
        "amount": 100_000_000,
        "status": ApprovalStatus.APPROVED_BY_ADMIN
    }
}

