import uuid
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schema.error import ErrorDetail
from app.schema.transaction_item import (
    TransactionItemCreate,
    TransactionItemPublic,
    TransactionItemUpdate
)
from app.services.transaction_item import transaction_item_service

router = APIRouter()

@router.post(
    "/", 
    response_model=TransactionItemPublic, 
    status_code=status.HTTP_201_CREATED,
    summary="Add an Item to a Draft Transaction",
    description="Creates a new transaction item and links it to an existing transaction. The parent transaction's total_price is automatically recalculated. Can only be done on transactions in 'draft' status.",
    responses={
        201: {"description": "Item added successfully."},
        400: {"model": ErrorDetail, "description": "Parent transaction is not in 'draft' status."},
        403: {"model": ErrorDetail, "description": "User does not have permission to modify the parent transaction."},
        404: {"model": ErrorDetail, "description": "Parent transaction or Item not found."},
    }
)
def create_transaction_item(
    item_in: TransactionItemCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin_or_user),
):
    """Adds a new line item to a transaction."""
    return transaction_item_service.create_item(db, item_in=item_in, current_user=current_user)

@router.put(
    "/{transaction_item_id}", 
    response_model=TransactionItemPublic,
    summary="Update an Item in a Draft Transaction",
    description="Updates an existing transaction item. The parent transaction's total_price is automatically recalculated. Can only be done on transactions in 'draft' status.",
    responses={
        200: {"description": "Item updated successfully."},
        400: {"model": ErrorDetail, "description": "Parent transaction is not in 'draft' status."},
        403: {"model": ErrorDetail, "description": "User does not have permission to modify the parent transaction."},
        404: {"model": ErrorDetail, "description": "Transaction item not found."},
    }
)
def update_transaction_item(
    transaction_item_id: uuid.UUID,
    item_in: TransactionItemUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin_or_user),
):
    """Updates a line item in a transaction."""
    return transaction_item_service.update_item(db, item_id=transaction_item_id, item_in=item_in, current_user=current_user)

@router.delete(
    "/{transaction_item_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an Item from a Draft Transaction",
    description="Deletes an existing transaction item. The parent transaction's total_price is automatically recalculated. Can only be done on transactions in 'draft' status.",
    responses={
        204: {"description": "Item deleted successfully."},
        400: {"model": ErrorDetail, "description": "Parent transaction is not in 'draft' status."},
        403: {"model": ErrorDetail, "description": "User does not have permission to modify the parent transaction."},
        404: {"model": ErrorDetail, "description": "Transaction item not found."},
    }
)
def delete_transaction_item(
    transaction_item_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin_or_user),
):
    """Deletes a line item from a transaction."""
    transaction_item_service.delete_item(db, item_id=transaction_item_id, current_user=current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

