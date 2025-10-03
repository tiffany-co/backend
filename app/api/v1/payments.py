from fastapi import APIRouter, Depends, Query, status, Response
from sqlalchemy.orm import Session
import uuid
from typing import List, Optional
from datetime import datetime

from app.api import deps
from app.models.user import User
from app.schema.payment import PaymentCreate, PaymentUpdate, PaymentPublic
from app.schema.error import ErrorDetail
from app.services.payment import payment_service
from app.models.enums.payment import PaymentMethod, PaymentDirection
from app.models.enums.shared import ApprovalStatus


router = APIRouter()

@router.post(
    "/",
    response_model=PaymentPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create Payment",
    description="Creates a new payment record in a 'draft' status.",
    responses={
        400: {"model": ErrorDetail, "description": "Bad Request (e.g., invalid logic, amount exceeds debt)"},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
        403: {"model": ErrorDetail, "description": "Forbidden (e.g., assigning photo holder to another user)"},
    }
)
def create_payment(
    payment_in: PaymentCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin_or_user),
):
    return payment_service.create(db=db, payment_in=payment_in, current_user=current_user)

@router.get(
    "/search",
    response_model=List[PaymentPublic],
    summary="Search Payments",
    description="Retrieves a list of payments with advanced filtering and sorting. Admins can see all payments, while users can only see payments they recorded.",
    responses={
        200: {"description": "A list of payments matching the search criteria."},
        401: {"model": ErrorDetail},
        403: {"model": ErrorDetail},
    }
)
def search_payments(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin_or_user),
    # Filters
    payment_method: Optional[PaymentMethod] = Query(None),
    direction: Optional[PaymentDirection] = Query(None),
    status: Optional[ApprovalStatus] = Query(None),
    photo_holder_id: Optional[uuid.UUID] = Query(None),
    investor_id: Optional[uuid.UUID] = Query(None),
    transaction_id: Optional[uuid.UUID] = Query(None),
    account_ledger_id: Optional[uuid.UUID] = Query(None),
    saved_bank_account_id: Optional[uuid.UUID] = Query(None),
    recorder_id: Optional[uuid.UUID] = Query(None, description="[Admin Only] Filter by the user who recorded the payment."),
    start_time: Optional[datetime] = Query(None, description="Search for payments created after this time."),
    end_time: Optional[datetime] = Query(None, description="Search for payments created before this time."),
    # Sorting
    amount: Optional[int] = Query(None, description="Sort results by the closest match to this amount."),
    # Pagination
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
):
    return payment_service.search(
        db,
        current_user=current_user,
        payment_method=payment_method,
        direction=direction,
        status=status,
        amount=amount,
        photo_holder_id=photo_holder_id,
        investor_id=investor_id,
        transaction_id=transaction_id,
        account_ledger_id=account_ledger_id,
        saved_bank_account_id=saved_bank_account_id,
        recorder_id=recorder_id,
        start_time=start_time,
        end_time=end_time,
        skip=skip,
        limit=limit
    )

@router.get(
    "/{payment_id}",
    response_model=PaymentPublic,
    summary="Get Payment by ID",
    description="Retrieves a single payment by its ID. Users can only retrieve payments they created.",
    responses={
        401: {"model": ErrorDetail},
        403: {"model": ErrorDetail},
        404: {"model": ErrorDetail},
    }
)
def get_payment_by_id(
    payment_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin_or_user),
):
    return payment_service.get_payment_by_id_and_check_permission(db, payment_id=payment_id, current_user=current_user)

@router.put(
    "/{payment_id}",
    response_model=PaymentPublic,
    summary="Update Payment",
    description="Updates a payment that is in 'draft' status. Users can only update payments they created.",
    responses={
        400: {"model": ErrorDetail, "description": "Bad Request (e.g., payment is not in draft status)"},
        401: {"model": ErrorDetail},
        403: {"model": ErrorDetail},
        404: {"model": ErrorDetail},
    }
)
def update_payment(
    payment_id: uuid.UUID,
    payment_in: PaymentUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin_or_user),
):
    return payment_service.update(db, payment_id=payment_id, payment_in=payment_in, current_user=current_user)

@router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Payment",
    description="Deletes a payment that is in 'draft' status. Users can only delete payments they created.",
    responses={
        400: {"model": ErrorDetail, "description": "Bad Request (e.g., payment is not in draft status)"},
        401: {"model": ErrorDetail},
        403: {"model": ErrorDetail},
        404: {"model": ErrorDetail},
    }
)
def delete_payment(
    payment_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin_or_user),
):
    payment_service.delete(db, payment_id=payment_id, current_user=current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post(
    "/{payment_id}/approve",
    response_model=PaymentPublic,
    summary="Approve a Payment",
    description="Advances the status of a payment. Users can approve from draft -> approved_by_user. Admins can approve from draft or approved_by_user -> approved_by_admin.",
    responses={
        400: {"model": ErrorDetail, "description": "Bad Request (e.g., payment cannot be approved further)"},
        401: {"model": ErrorDetail},
        403: {"model": ErrorDetail},
        404: {"model": ErrorDetail},
    }
)
def approve_payment(
    payment_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin_or_user),
):
    return payment_service.approve(db, payment_id=payment_id, current_user=current_user)

@router.post(
    "/{payment_id}/reject",
    response_model=PaymentPublic,
    summary="Reject a Payment",
    description="Returns a payment to 'draft' status. Users can reject from approved_by_user. Admins can reject from approved_by_user or approved_by_admin.",
    responses={
        400: {"model": ErrorDetail, "description": "Bad Request (e.g., draft payment cannot be rejected)"},
        401: {"model": ErrorDetail},
        403: {"model": ErrorDetail},
        404: {"model": ErrorDetail},
    }
)
def reject_payment(
    payment_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin_or_user),
):
    return payment_service.reject(db, payment_id=payment_id, current_user=current_user)

