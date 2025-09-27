from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional, Any
import uuid

from app.repository.base import BaseRepository
from app.models.payment import Payment
from app.models.user import User, UserRole
from app.models.enums.payment import PaymentMethod, PaymentDirection
from app.models.enums.shared import ApprovalStatus
from app.schema.payment import PaymentCreate, PaymentUpdate

class PaymentRepository(BaseRepository[Payment, PaymentCreate, PaymentUpdate]):
    """Repository for payment-related database operations."""

    def search(
        self,
        db: Session,
        *,
        current_user: User,
        payment_method: Optional[PaymentMethod] = None,
        direction: Optional[PaymentDirection] = None,
        status: Optional[ApprovalStatus] = None,
        amount: Optional[int] = None,
        photo_holder_id: Optional[uuid.UUID] = None,
        investment_id: Optional[uuid.UUID] = None,
        transaction_id: Optional[uuid.UUID] = None,
        account_ledger_id: Optional[uuid.UUID] = None,
        saved_bank_account_id: Optional[uuid.UUID] = None,
        recorder_id: Optional[uuid.UUID] = None,
        skip: int,
        limit: int
    ) -> List[Payment]:
        """
        Searches for payments based on a combination of criteria with advanced sorting.
        """
        query = db.query(self.model)

        # Non-admins can only see payments they recorded.
        if current_user.role != UserRole.ADMIN:
            query = query.filter(Payment.recorder_id == current_user.id)
        elif recorder_id: # Admins can filter by recorder
            query = query.filter(Payment.recorder_id == recorder_id)

        # Apply filters
        if payment_method:
            query = query.filter(Payment.payment_method == payment_method)
        if direction:
            query = query.filter(Payment.direction == direction)
        if status:
            query = query.filter(Payment.status == status)
        if photo_holder_id:
            query = query.filter(Payment.photo_holder_id == photo_holder_id)
        if investment_id:
            query = query.filter(Payment.investment_id == investment_id)
        if transaction_id:
            query = query.filter(Payment.transaction_id == transaction_id)
        if account_ledger_id:
            query = query.filter(Payment.account_ledger_id == account_ledger_id)
        if saved_bank_account_id:
            query = query.filter(Payment.saved_bank_account_id == saved_bank_account_id)

        # Conditional Sorting
        if amount is not None:
            # Order by the absolute difference from the provided amount
            query = query.order_by(func.abs(self.model.amount - amount).asc())
        else:
            # Default sort by the most recent payment
            query = query.order_by(desc(self.model.created_at))
            
        return query.offset(skip).limit(limit).all()

payment_repo = PaymentRepository(Payment)

