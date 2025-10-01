from sqlalchemy.orm import Session
from app.repository.base import BaseRepository
from app.models.investment import Investment
from typing import Any, Optional, List
import uuid

class InvestmentRepository(BaseRepository[Investment, Any, Any]):
    """Repository for Investment model operations."""

    def get_by_payment_id(self, db: Session, *, payment_id: Any) -> Investment | None:
        """Find an investment record linked to a specific payment ID."""
        return db.query(self.model).filter(self.model.payment_id == payment_id).first()

    def search(
        self,
        db: Session,
        *,
        investor_id: Optional[uuid.UUID] = None,
        min_amount: Optional[int] = None,
        max_amount: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Investment]:
        """
        Searches for investments based on a combination of criteria.
        """
        query = db.query(self.model)

        if investor_id:
            query = query.filter(self.model.investor_id == investor_id)
        if min_amount is not None:
            query = query.filter(self.model.amount >= min_amount)
        if max_amount is not None:
            query = query.filter(self.model.amount <= max_amount)

        return query.order_by(self.model.created_at.desc()).offset(skip).limit(limit).all()

investment_repo = InvestmentRepository(Investment)
