from sqlalchemy.orm import Session
from app.repository.base import BaseRepository
from app.models.investment import Investment
from typing import Any

class InvestmentRepository(BaseRepository[Investment, Any, Any]):
    """Repository for Investment model operations."""

    def get_by_payment_id(self, db: Session, *, payment_id: Any) -> Investment | None:
        """Find an investment record linked to a specific payment ID."""
        return db.query(self.model).filter(self.model.payment_id == payment_id).first()

investment_repo = InvestmentRepository(Investment)
