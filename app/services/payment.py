from sqlalchemy.orm import Session
import uuid
from typing import List, Any

from app.core.exceptions import AppException
from fastapi import status
from app.models.user import User, UserRole
from app.models.payment import Payment, PaymentDirection
from app.models.enums.shared import ApprovalStatus
from app.repository.payment import payment_repo
from app.schema.payment import PaymentCreate, PaymentUpdate
from app.services.inventory import inventory_service
from app.services.account_ledger import account_ledger_service

class PaymentService:
    """Service layer for payment-related business logic."""

    def get_payment_by_id_and_check_permission(self, db: Session, *, payment_id: uuid.UUID, current_user: User) -> Payment:
        """Helper to get a payment by ID and verify user has permission to view it."""
        payment = payment_repo.get(db, id=payment_id)
        if not payment:
            raise AppException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Payment with ID {payment_id} not found.")
        
        is_owner = payment.recorder_id == current_user.id
        is_admin = current_user.role == UserRole.ADMIN

        if not is_owner and not is_admin:
            raise AppException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this payment.")
            
        return payment

    def search(
        self,
        db: Session,
        *,
        current_user: User,
        **kwargs: Any
    ) -> List[Payment]:
        """Orchestrates the search for payments by calling the repository."""
        return payment_repo.search(
            db,
            current_user=current_user,
            **kwargs
        )

    def create(self, db: Session, *, payment_in: PaymentCreate, current_user: User) -> Payment:
        """Handles business logic for creating a new payment."""
        payment_data = payment_in.model_dump()
        payment_data["recorder_id"] = current_user.id

        if payment_in.photo_holder_id and payment_in.photo_holder_id != current_user.id and current_user.role != UserRole.ADMIN:
            raise AppException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only assign yourself as the photo holder.")
        
        if payment_in.account_ledger_id:
            ledger = account_ledger_service.get_by_id(db, account_ledger_id=payment_in.account_ledger_id)
            if payment_in.amount > ledger.debt and payment_in.direction != PaymentDirection.INCOMING:
                raise AppException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment amount cannot be greater than the outstanding debt.")

        return payment_repo.create(db, obj_in=payment_data)

    def update(self, db: Session, *, payment_id: uuid.UUID, payment_in: PaymentUpdate, current_user: User) -> Payment:
        """Handles business logic for updating a payment."""
        payment = self.get_payment_by_id_and_check_permission(db, payment_id=payment_id, current_user=current_user)

        if payment.status != ApprovalStatus.DRAFT:
            raise AppException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only payments in 'draft' status can be updated.")

        return payment_repo.update(db, db_obj=payment, obj_in=payment_in)

    def delete(self, db: Session, *, payment_id: uuid.UUID, current_user: User):
        """Handles business logic for deleting a payment."""
        payment = self.get_payment_by_id_and_check_permission(db, payment_id=payment_id, current_user=current_user)

        if payment.status != ApprovalStatus.DRAFT:
            raise AppException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only payments in 'draft' status can be deleted.")
        
        return payment_repo.remove(db, id=payment.id)

    def approve(self, db: Session, *, payment_id: uuid.UUID, current_user: User) -> Payment:
        """Handles the logic for approving a payment and advancing its status."""
        payment = self.get_payment_by_id_and_check_permission(db, payment_id=payment_id, current_user=current_user)
        
        new_status = self._get_next_approval_status(payment.status, current_user.role)
        self._handle_side_effects(db, payment, old_status=payment.status, new_status=new_status)

        payment.status = new_status
        db.commit()
        db.refresh(payment)
        return payment

    def reject(self, db: Session, *, payment_id: uuid.UUID, current_user: User) -> Payment:
        """Handles the logic for rejecting a payment and returning it to draft."""
        payment = self.get_payment_by_id_and_check_permission(db, payment_id=payment_id, current_user=current_user)
        
        old_status = payment.status
        if old_status == ApprovalStatus.DRAFT:
             raise AppException(status_code=status.HTTP_400_BAD_REQUEST, detail="Draft payments cannot be rejected.")

        is_admin = current_user.role == UserRole.ADMIN
        if not is_admin and old_status == ApprovalStatus.APPROVED_BY_ADMIN:
            raise AppException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to reject this payment.")
        
        self._handle_side_effects(db, payment, old_status=old_status, new_status=ApprovalStatus.DRAFT)
        
        payment.status = ApprovalStatus.DRAFT
        db.commit()
        db.refresh(payment)
        return payment
        
    def _get_next_approval_status(self, current_status: ApprovalStatus, user_role: UserRole) -> ApprovalStatus:
        """Determines the next valid status for a payment upon approval."""
        is_admin = user_role == UserRole.ADMIN
        
        if current_status == ApprovalStatus.DRAFT:
            return ApprovalStatus.APPROVED_BY_ADMIN if is_admin else ApprovalStatus.APPROVED_BY_USER
        
        if current_status == ApprovalStatus.APPROVED_BY_USER and is_admin:
            return ApprovalStatus.APPROVED_BY_ADMIN
        
        raise AppException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment cannot be approved further.")

    def _handle_side_effects(self, db: Session, payment: Payment, old_status: ApprovalStatus, new_status: ApprovalStatus):
        """Orchestrates ledger and inventory updates based on status changes."""
        is_approving = new_status != ApprovalStatus.DRAFT
        was_admin_approved = old_status == ApprovalStatus.APPROVED_BY_ADMIN
        is_becoming_admin_approved = new_status == ApprovalStatus.APPROVED_BY_ADMIN

        # --- Ledger Updates ---
        if payment.account_ledger_id:
            if is_approving and old_status == ApprovalStatus.DRAFT: # First time approval
                account_ledger_service.update_debt_from_payment(db, payment=payment)
            elif not is_approving and old_status != ApprovalStatus.DRAFT: # Any rejection
                account_ledger_service.revert_debt_from_payment(db, payment=payment)
        
        # --- Inventory (Money Balance) Updates ---
        if payment.direction != PaymentDirection.INTERNAL_TRANSFER:
            if is_becoming_admin_approved:
                inventory_service.update_money_balance_from_payment(db, payment=payment)
            elif not is_approving and was_admin_approved:
                inventory_service.revert_money_balance_from_payment(db, payment=payment)

payment_service = PaymentService()

