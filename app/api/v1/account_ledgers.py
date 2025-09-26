from fastapi import APIRouter, Depends, Query, status, Response
from sqlalchemy.orm import Session
import uuid
from typing import List, Optional

from app.api import deps
from app.models.user import User
from app.schema.account_ledger import AccountLedgerCreate, AccountLedgerUpdate, AccountLedgerPublic
from app.schema.error import ErrorDetail
from app.services.account_ledger import account_ledger_service

router = APIRouter()

@router.post(
    "/",
    response_model=AccountLedgerPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create Account Ledger Entry",
    description="Allows an authenticated user to create a new account ledger entry for one of their contacts.",
    responses={
        201: {"description": "Ledger entry created successfully."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
        403: {"model": ErrorDetail, "description": "User does not have permission for the specified contact."},
        404: {"model": ErrorDetail, "description": "Contact or Transaction not found."},
    }
)
def create_account_ledger(
    ledger_in: AccountLedgerCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return account_ledger_service.create(db=db, ledger_in=ledger_in, current_user=current_user)

@router.get(
    "/search",
    response_model=List[AccountLedgerPublic],
    summary="Search Account Ledger Entries",
    description="Search and filter account ledger entries. Admins can search all entries; users can only search within their own contacts.",
    responses={
        200: {"description": "A list of account ledger entries matching the criteria."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
    }
)
def search_account_ledgers(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    has_debt: Optional[bool] = Query(None, description="Set to 'true' to find entries with a non-zero debt."),
    bank_name: Optional[str] = Query(None, description="Filter by bank name (case-insensitive, partial match)."),
    contact_id: Optional[uuid.UUID] = Query(None, description="Filter by a specific contact ID."),
    transaction_id: Optional[uuid.UUID] = Query(None, description="Filter by a specific transaction ID."),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
):
    return account_ledger_service.search(
        db,
        has_debt=has_debt,
        bank_name=bank_name,
        contact_id=contact_id,
        transaction_id=transaction_id,
        skip=skip,
        limit=limit
    )

@router.get(
    "/{ledger_id}",
    response_model=AccountLedgerPublic,
    summary="Get Account Ledger Entry by ID",
    description="Retrieves a single account ledger entry by its unique ID.",
    responses={
        200: {"description": "The requested account ledger entry."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
        403: {"model": ErrorDetail, "description": "User does not have permission to view this entry."},
        404: {"model": ErrorDetail, "description": "Ledger entry not found."},
    }
)
def get_account_ledger_by_id(
    ledger_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return account_ledger_service.get_by_id(db, ledger_id=ledger_id)

@router.put(
    "/{ledger_id}",
    response_model=AccountLedgerPublic,
    summary="Update Account Ledger Entry",
    description="Updates the details of a specific account ledger entry.",
    responses={
        200: {"description": "Ledger entry updated successfully."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
        403: {"model": ErrorDetail, "description": "User does not have permission to update this entry."},
        404: {"model": ErrorDetail, "description": "Ledger entry not found."},
    }
)
def update_account_ledger(
    ledger_id: uuid.UUID,
    ledger_in: AccountLedgerUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return account_ledger_service.update(db, ledger_id=ledger_id, ledger_in=ledger_in)

@router.delete(
    "/{ledger_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Account Ledger Entry",
    description="Deletes a specific account ledger entry.",
    responses={
        204: {"description": "Ledger entry deleted successfully."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
        403: {"model": ErrorDetail, "description": "User does not have permission to delete this entry."},
        404: {"model": ErrorDetail, "description": "Ledger entry not found."},
    }
)
def delete_account_ledger(
    ledger_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    account_ledger_service.delete(db, ledger_id=ledger_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
