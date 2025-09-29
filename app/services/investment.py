import uuid
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from fastapi import status
from app.models.investment import Investment
from app.repository.investment import investment_repo

class InvestmentService:
    """
    Service layer for investment-related business logic.
    Currently a placeholder to support FK validation.
    """
    def get_by_id(self, db: Session, *, investment_id: uuid.UUID) -> Investment:
        """Helper method to get an investment by ID or raise 404."""
        investment = investment_repo.get(db, id=investment_id)
        if not investment:
            raise AppException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Investment with ID {investment_id} not found.")
        return investment

investment_service = InvestmentService()
