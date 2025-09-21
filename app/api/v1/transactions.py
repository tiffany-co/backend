import uuid
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.models.enums.transaction import TransactionStatus, TransactionType
from app.schema.transaction import (
    TransactionCreate, 
    TransactionPublic, 
    TransactionUpdate, 
    TransactionWithItemsPublic
)
from app.services.transaction import transaction_service

router = APIRouter()

@router.post("/", response_model=TransactionPublic, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction_in: TransactionCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return transaction_service.create_transaction(db, transaction_in=transaction_in, current_user=current_user)

@router.get("/search", response_model=List[TransactionPublic])
def search_transactions(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    recorder_id: Optional[uuid.UUID] = Query(None),
    contact_id: Optional[uuid.UUID] = Query(None),
    status: Optional[TransactionStatus] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    item_title: Optional[str] = Query(None),
    item_id: Optional[uuid.UUID] = Query(None),
    item_transaction_type: Optional[TransactionType] = Query(None),
    skip: int = 0,
    limit: int = 100,
):
    return transaction_service.search_transactions(
        db, current_user=current_user, recorder_id=recorder_id, contact_id=contact_id, status=status,
        start_time=start_time, end_time=end_time, item_title=item_title, item_id=item_id,
        item_transaction_type=item_transaction_type, skip=skip, limit=limit
    )

@router.get("/search/detailed", response_model=List[TransactionWithItemsPublic])
def search_transactions_detailed(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    recorder_id: Optional[uuid.UUID] = Query(None),
    contact_id: Optional[uuid.UUID] = Query(None),
    status: Optional[TransactionStatus] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    item_title: Optional[str] = Query(None),
    item_id: Optional[uuid.UUID] = Query(None),
    item_transaction_type: Optional[TransactionType] = Query(None),
    skip: int = 0,
    limit: int = 100,
):
    return transaction_service.search_transactions(
        db, current_user=current_user, recorder_id=recorder_id, contact_id=contact_id, status=status,
        start_time=start_time, end_time=end_time, item_title=item_title, item_id=item_id,
        item_transaction_type=item_transaction_type, skip=skip, limit=limit
    )

@router.get("/{transaction_id}", response_model=TransactionWithItemsPublic)
def get_transaction(
    transaction_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return transaction_service.get_transaction_by_id(db, transaction_id=transaction_id, current_user=current_user, with_items=True)

@router.put("/{transaction_id}", response_model=TransactionPublic)
def update_transaction(
    transaction_id: uuid.UUID,
    transaction_in: TransactionUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return transaction_service.update_transaction(db, transaction_id=transaction_id, transaction_in=transaction_in, current_user=current_user)

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    transaction_service.delete_transaction(db, transaction_id=transaction_id, current_user=current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/{transaction_id}/approve", response_model=TransactionPublic)
def approve_transaction(
    transaction_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return transaction_service.approve_transaction(db, transaction_id=transaction_id, current_user=current_user)

@router.post("/{transaction_id}/reject", response_model=TransactionPublic)
def reject_transaction(
    transaction_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return transaction_service.reject_transaction(db, transaction_id=transaction_id, current_user=current_user)
