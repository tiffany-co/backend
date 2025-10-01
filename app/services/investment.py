import uuid
from sqlalchemy.orm import Session
from fastapi import status

from app.core.exceptions import AppException
from app.models.investment import Investment
from app.models.payment import Payment
from app.repository.investment import investment_repo

class InvestmentService:
    """Service layer for investment-related business logic."""
    
    def get_by_id(self, db: Session, *, investment_id: uuid.UUID) -> Investment:
        investment = investment_repo.get(db, id=investment_id)
        if not investment:
            raise AppException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Investment with ID {investment_id} not found.")
        return investment
    
    def create_from_payment(self, db: Session, *, payment: Payment) -> Investment:
        """Creates an Investment record from an approved incoming payment."""
        if not payment.investor_id:
            return None

        new_investment = investment_repo.create(db, obj_in={
            "amount": payment.amount,
            "investor_id": payment.investor_id,
            "payment_id": payment.id
        })
        return new_investment
        
    def delete_by_payment_id(self, db: Session, *, payment_id: uuid.UUID):
        """Deletes an investment record when its associated payment is rejected."""
        investment_to_delete = investment_repo.get_by_payment_id(db, payment_id=payment_id)
        if investment_to_delete:
            investment_repo.remove(db, id=investment_to_delete.id)


investment_service = InvestmentService()
