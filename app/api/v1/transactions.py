import uuid
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.models.enums.transaction import TransactionType
from app.models.enums.shared import ApprovalStatus
from app.schema.transaction import (
    TransactionCreate, 
    TransactionPublic, 
    TransactionUpdate, 
    TransactionWithItemsPublic
)
from app.schema.error import ErrorDetail
from app.services.transaction import transaction_service

router = APIRouter()

@router.post(
    "/", 
    response_model=TransactionPublic, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a New Transaction",
    description="Creates a new transaction record in a 'draft' state. Transaction items must be added in subsequent calls.",
    responses={
        201: {"description": "Transaction created successfully."},
        401: {"model": ErrorDetail, "description": "User is not authenticated."},
        404: {"model": ErrorDetail, "description": "The specified contact_id was not found."},
    }
)
def create_transaction(
    transaction_in: TransactionCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Creates the initial transaction entry. Items are added separately."""
    return transaction_service.create_transaction(db, transaction_in=transaction_in, current_user=current_user)

@router.get(
    "/search", 
    response_model=List[TransactionPublic],
    summary="Search Transactions (Basic View)",
    description="Searches for transactions based on various criteria. This view does NOT include transaction items for performance."
)
def search_transactions(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    recorder_id: Optional[uuid.UUID] = Query(None, description="Filter by the user who recorded the transaction."),
    contact_id: Optional[uuid.UUID] = Query(None, description="Filter by the contact associated with the transaction."),
    status: Optional[ApprovalStatus] = Query(None, description="Filter by transaction status."),
    start_time: Optional[datetime] = Query(None, description="ISO 8601 format. e.g., 2025-09-20T10:00:00"),
    end_time: Optional[datetime] = Query(None, description="ISO 8601 format. e.g., 2025-09-21T10:00:00"),
    item_title: Optional[str] = Query(None, description="Find transactions containing an item with this title (partial match)."),
    item_id: Optional[uuid.UUID] = Query(None, description="Find transactions containing a specific item ID."),
    item_transaction_type: Optional[TransactionType] = Query(None, description="Find transactions containing a specific item transaction type."),
    skip: int = 0,
    limit: int = 100,
):
    """Admin can search all transactions. Regular users can only search their own."""
    return transaction_service.search_transactions(
        db, current_user=current_user, recorder_id=recorder_id, contact_id=contact_id, status=status,
        start_time=start_time, end_time=end_time, item_title=item_title, item_id=item_id,
        item_transaction_type=item_transaction_type, skip=skip, limit=limit
    )

@router.get(
    "/search/detailed", 
    response_model=List[TransactionWithItemsPublic],
    summary="Search Transactions (Detailed View)",
    description="Searches for transactions based on various criteria. This view INCLUDES the list of transaction items."
)
def search_transactions_detailed(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    recorder_id: Optional[uuid.UUID] = Query(None, description="Filter by the user who recorded the transaction."),
    contact_id: Optional[uuid.UUID] = Query(None, description="Filter by the contact associated with the transaction."),
    status: Optional[ApprovalStatus] = Query(None, description="Filter by transaction status."),
    start_time: Optional[datetime] = Query(None, description="ISO 8601 format. e.g., 2025-09-20T10:00:00"),
    end_time: Optional[datetime] = Query(None, description="ISO 8601 format. e.g., 2025-09-21T10:00:00"),
    item_title: Optional[str] = Query(None, description="Find transactions containing an item with this title (partial match)."),
    item_id: Optional[uuid.UUID] = Query(None, description="Find transactions containing a specific item ID."),
    item_transaction_type: Optional[TransactionType] = Query(None, description="Find transactions containing a specific item transaction type."),
    skip: int = 0,
    limit: int = 100,
):
    """Admin can search all transactions. Regular users can only search their own."""
    return transaction_service.search_transactions(
        db, current_user=current_user, recorder_id=recorder_id, contact_id=contact_id, status=status,
        start_time=start_time, end_time=end_time, item_title=item_title, item_id=item_id,
        item_transaction_type=item_transaction_type, skip=skip, limit=limit
    )

@router.get(
    "/{transaction_id}", 
    response_model=TransactionWithItemsPublic,
    summary="Get a Single Transaction",
    description="Retrieves a single transaction by its ID, including all of its items.",
    responses={
        200: {"description": "The requested transaction."},
        403: {"model": ErrorDetail, "description": "User does not have permission to view this transaction."},
        404: {"model": ErrorDetail, "description": "Transaction not found."},
    }
)
def get_transaction(
    transaction_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Retrieves a specific transaction, checking for ownership if the user is not an admin."""
    return transaction_service.get_transaction_by_id(db, transaction_id=transaction_id, current_user=current_user, with_items=True)

@router.put(
    "/{transaction_id}",
    response_model=TransactionPublic,
    summary="Update a Draft Transaction",
    description="Updates the contact, note, or discount on a transaction that is still in 'draft' status.",
    responses={
        200: {"description": "Transaction updated successfully."},
        400: {"model": ErrorDetail, "description": "Transaction is not in draft status."},
        403: {"model": ErrorDetail, "description": "User does not have permission to update this transaction."},
        404: {"model": ErrorDetail, "description": "Transaction or Contact not found."},
    }
)
def update_transaction(
    transaction_id: uuid.UUID,
    transaction_in: TransactionUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Allows modification only if the transaction status is 'draft'."""
    return transaction_service.update_transaction(db, transaction_id=transaction_id, transaction_in=transaction_in, current_user=current_user)

@router.delete(
    "/{transaction_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a Draft Transaction",
    description="Deletes a transaction that is still in 'draft' status. All associated items will also be deleted.",
     responses={
        204: {"description": "Transaction deleted successfully."},
        400: {"model": ErrorDetail, "description": "Transaction is not in draft status and cannot be deleted."},
        403: {"model": ErrorDetail, "description": "User does not have permission to delete this transaction."},
        404: {"model": ErrorDetail, "description": "Transaction not found."},
    }
)
def delete_transaction(
    transaction_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Performs a deletion only if the transaction status is 'draft'."""
    transaction_service.delete_transaction(db, transaction_id=transaction_id, current_user=current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post(
    "/{transaction_id}/approve", 
    response_model=TransactionPublic,
    summary="Approve a Transaction",
    description="""
    Advances the status of a transaction.
    - **User**: Can advance a 'draft' transaction to 'approved_by_user'.
    - **Admin**: Can advance a 'draft' or 'approved_by_user' transaction to 'approved_by_admin'. This will trigger an inventory update.
    """
)
def approve_transaction(
    transaction_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Handles the state transition for approving a transaction based on user role."""
    return transaction_service.approve_transaction(db, transaction_id=transaction_id, current_user=current_user)

@router.post(
    "/{transaction_id}/reject", 
    response_model=TransactionPublic,
    summary="Reject a Transaction",
    description="""
    Returns a transaction to the 'draft' status.
    - **User**: Can reject a transaction they have previously set to 'approved_by_user'.
    - **Admin**: Can reject any 'approved_by_user' or 'approved_by_admin' transaction. Rejecting an 'approved_by_admin' transaction will trigger a reversing inventory update.
    """
)
def reject_transaction(
    transaction_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Handles the state transition for rejecting a transaction based on user role."""
    return transaction_service.reject_transaction(db, transaction_id=transaction_id, current_user=current_user)

