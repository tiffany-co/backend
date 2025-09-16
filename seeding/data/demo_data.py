from app.models.enums.user import UserRole
from app.models.enums.contact import ContactType
from app.schema.user import UserCreate, AdminCreate
from app.schema.contact import ContactCreate
from app.schema.saved_bank_account import SavedBankAccountCreate

# This file contains sample data for populating the database for a demo.

DEMO_USERS = [
    AdminCreate(
        full_name="حسین عجمی",
        username='admin',
        phone_number='09215256536',
        is_active=True,
        password='11111111',
        role=UserRole.ADMIN
    ),
    UserCreate(
        full_name="رضا فراستی",
        username="reza",
        phone_number="09121112233",
        password="11111111",
    ),
    UserCreate(
        full_name="علی رضایی",
        username="ali",
        phone_number="09124445566",
        password="11111111",
    ),
]

DEMO_CONTACTS = [
    {
        "owner_username": "admin", # Assign this contact to the admin user
        "contact": ContactCreate(
            first_name="Farhad",
            last_name="Ahmadi",
            phone_number="09151234567",
            national_number="9876543210",
            type=ContactType.CUSTOMER,
        ),
    },
    {
        "owner_username": "reza", # Assign this contact to reza
        "contact": ContactCreate(
            first_name="Maryam",
            last_name="Rezai",
            phone_number="09157654321",
            national_number="1234567891",
            type=ContactType.CUSTOMER,
        ),
    },
]

# --- NEW: Demo data for Saved Bank Accounts ---
DEMO_SAVED_BANK_ACCOUNTS = [
    SavedBankAccountCreate(
        name="بانک ملت آقای رضایی",
        description="این حساب متعلق به آقای رضایی اصل است",
        card_number="6104337811112222"
    ),
    SavedBankAccountCreate(
        name="بانک صادرات مجید دلاوری",
        description="این حساب متعلق به آقای مجید دلاوری است",
        card_number="6037691122223333"
    ),
    SavedBankAccountCreate(
        name="بانک ملی سوییس",
        description="بانک سوییس، شماره حساب 155698",
        card_number=None # An account doesn't need a card number
    )
]