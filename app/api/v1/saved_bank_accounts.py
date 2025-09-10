from fastapi import APIRouter, Depends, status, Query, Response
from sqlalchemy.orm import Session
import uuid
from typing import List

from app.api import deps
from app.models.user import User, UserRole
from app.schema.saved_bank_account import (
    SavedBankAccountCreate,
    SavedBankAccountPublic,
    SavedBankAccountUpdate,
)
from app.schema.error import ErrorDetail
from app.services.saved_bank_account import saved_bank_account_service

router = APIRouter()

@router.post(
    "/",
    response_model=SavedBankAccountPublic,
    status_code=status.HTTP_201_CREATED,
    summary="[Admin] Create Saved Bank Account",
    description="Allows an administrator to create a new saved bank account.",
    responses={
        201: {"description": "Bank account created successfully."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
        403: {"model": ErrorDetail, "description": "Forbidden"},
        409: {"model": ErrorDetail, "description": "Conflict (e.g., name or card number already exists)"},
    }
)
def create_saved_bank_account(
    account_in: SavedBankAccountCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
):
    return saved_bank_account_service.create(db=db, account_in=account_in, current_user=current_user)


@router.get(
    "/",
    response_model=List[SavedBankAccountPublic],
    summary="Get All Saved Bank Accounts",
    description="Allows any authenticated user to retrieve a paginated list of all saved bank accounts.",
     responses={
        200: {"description": "A list of saved bank accounts."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
    }
)
def read_all_saved_bank_accounts(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
):
    return saved_bank_account_service.get_all(db, skip=skip, limit=limit)


@router.get(
    "/{account_id}",
    response_model=SavedBankAccountPublic,
    summary="Get Saved Bank Account by ID",
    description="Allows any authenticated user to fetch a single saved bank account by its ID.",
     responses={
        200: {"description": "The requested bank account."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
        404: {"model": ErrorDetail, "description": "Bank account not found"},
    }
)
def read_saved_bank_account_by_id(
    account_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return saved_bank_account_service.get_by_id(db, account_id=account_id)


@router.put(
    "/{account_id}",
    response_model=SavedBankAccountPublic,
    summary="[Admin] Update Saved Bank Account",
    description="Allows an administrator to update a saved bank account.",
    responses={
        200: {"description": "Bank account updated successfully."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
        403: {"model": ErrorDetail, "description": "Forbidden"},
        404: {"model": ErrorDetail, "description": "Bank account not found"},
        409: {"model": ErrorDetail, "description": "Conflict (e.g., name or card number already exists)"},
    }
)
def update_saved_bank_account(
    account_id: uuid.UUID,
    account_in: SavedBankAccountUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
):
    return saved_bank_account_service.update(db=db, account_id=account_id, account_in=account_in, current_user=current_user)


@router.delete(
    "/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="[Admin] Delete Saved Bank Account",
    description="Allows an administrator to delete a saved bank account.",
    responses={
        204: {"description": "Bank account deleted successfully."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
        403: {"model": ErrorDetail, "description": "Forbidden"},
        404: {"model": ErrorDetail, "description": "Bank account not found"},
    }
)
def delete_saved_bank_account(
    account_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
):
    saved_bank_account_service.delete(db, account_id=account_id, current_user=current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
