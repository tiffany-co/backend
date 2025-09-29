from app.repository.base import BaseRepository
from app.models.investment import Investment
from typing import Any

class InvestmentRepository(BaseRepository[Investment, Any, Any]):
    """
    Repository for Investment model operations.
    Currently a placeholder to support FK validation.
    """
    pass

investment_repo = InvestmentRepository(Investment)
