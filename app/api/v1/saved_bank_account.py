from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.api import deps
from app.models.user import UserRole
from app.schema.saved_bank_account import (
    SavedBankAccountCreate,
    SavedBankAccountPublic,
    SavedBankAccountUpdate,
)
from app.services.saved_bank_account import saved_bank_account_service
from app.repository.saved_bank_account import saved_bank_account_repo

router = APIRouter()

# Dependency for requiring admin role
require_admin = deps.require_role([UserRole.ADMIN])

@router.post(
    "/",
    response_model=SavedBankAccountPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
def create_saved_bank_account(
    *,
    db: Session = Depends(deps.get_db),
    bank_account_in: SavedBankAccountCreate,
):
    """
    Create a new saved bank account. (Admin only)
    """
    return saved_bank_account_service.create(db=db, obj_in=bank_account_in)

@router.get("/", response_model=List[SavedBankAccountPublic])
def read_all_saved_bank_accounts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(deps.get_current_active_user), # QUESTION: we we put this line on decorator?
):
    """
    Retrieve all saved bank accounts. (All authenticated users)
    """
    return saved_bank_account_repo.get_multi(db, skip=skip, limit=limit)

@router.get("/{account_id}", response_model=SavedBankAccountPublic)
def read_saved_bank_account_by_id(
    account_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_active_user),
):
    """
    Retrieve a specific saved bank account by its ID. (All authenticated users)
    """
    account = saved_bank_account_repo.get(db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bank account not found"
        )
    return account

@router.put(
    "/{account_id}",
    response_model=SavedBankAccountPublic,
    dependencies=[Depends(require_admin)],
)
def update_saved_bank_account(
    account_id: uuid.UUID,
    bank_account_in: SavedBankAccountUpdate,
    db: Session = Depends(deps.get_db),
):
    """
    Update a saved bank account. (Admin only)
    """
    account = saved_bank_account_repo.get(db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bank account not found"
        )
    return saved_bank_account_service.update(db=db, db_obj=account, obj_in=bank_account_in)

@router.delete(
    "/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_saved_bank_account(
    account_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
):
    """
    Delete a saved bank account. (Admin only)
    """
    account = saved_bank_account_repo.get(db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bank account not found"
        )
    saved_bank_account_repo.remove(db, id=account_id)
    return
