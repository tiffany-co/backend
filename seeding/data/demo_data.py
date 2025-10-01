from app.models.enums.user import UserRole
from app.models.enums.contact import ContactType
from app.schema.user import UserCreate, AdminCreate
from app.schema.contact import ContactCreate
from app.schema.saved_bank_account import SavedBankAccountCreate
from app.schema.inventory import InventoryAdjust, InventoryItemsSchema
from app.schema.investor import InvestorCreate
from .scenarios import ALL_SCENARIOS

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

DEMO_INVESTORS = [
    {
        "creator_username": "admin",
        "investor": InvestorCreate(
            first_name="سارا",
            last_name="محمدی",
            phone_number="09351112233",
            national_number="1112223334",
            username="sara",
            password="11111111"
        )
    }
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

# A list of all scenarios to be run by the seeder script.
DEMO_SCENARIOS = ALL_SCENARIOS

