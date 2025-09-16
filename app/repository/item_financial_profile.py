from sqlalchemy.orm import Session
from app.repository.base import BaseRepository
from app.models.item_financial_profile import ItemFinancialProfile
from app.schema.item_financial_profile import ItemFinancialProfileCreate, ItemFinancialProfileUpdate

class ItemFinancialProfileRepository(BaseRepository[ItemFinancialProfile, ItemFinancialProfileCreate, ItemFinancialProfileUpdate]):
    """
    Repository for item financial profile related database operations.
    """
    pass

item_financial_profile_repo = ItemFinancialProfileRepository(ItemFinancialProfile)
