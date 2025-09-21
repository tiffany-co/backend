import uuid
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schema.transaction_item import (
    TransactionItemCreate,
    TransactionItemPublic,
    TransactionItemUpdate
)
from app.services.transaction_item import transaction_item_service

router = APIRouter()

@router.post("/", response_model=TransactionItemPublic, status_code=status.HTTP_201_CREATED)
def create_transaction_item(
    item_in: TransactionItemCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return transaction_item_service.create_item(db, item_in=item_in, current_user=current_user)

@router.put("/{item_id}", response_model=TransactionItemPublic)
def update_transaction_item(
    item_id: uuid.UUID,
    item_in: TransactionItemUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return transaction_item_service.update_item(db, item_id=item_id, item_in=item_in, current_user=current_user)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction_item(
    item_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    transaction_item_service.delete_item(db, item_id=item_id, current_user=current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
