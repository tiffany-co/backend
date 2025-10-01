from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
import uuid
from typing import List, Optional

from app.api import deps
from app.models.user import User, UserRole
from app.schema.investment import InvestmentPublic
from app.schema.error import ErrorDetail
from app.services.investment import investment_service

router = APIRouter()

@router.get(
    "/{investment_id}",
    response_model=InvestmentPublic,
    summary="[Admin] Get Investment by ID",
    description="Allows an administrator to fetch a single investment by its unique ID.",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
    responses={
        200: {"description": "The requested investment record."},
        401: {"model": ErrorDetail},
        403: {"model": ErrorDetail},
        404: {"model": ErrorDetail, "description": "Investment not found"},
    }
)
def get_investment_by_id(
    investment_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
):
    return investment_service.get_by_id(db, investment_id=investment_id)

@router.get(
    "/",
    response_model=List[InvestmentPublic],
    summary="Search Investments",
    description="Allows Admins and regular Users to search for investment records.",
    responses={
        200: {"description": "A list of investments matching the criteria."},
        401: {"model": ErrorDetail},
        403: {"model": ErrorDetail},
    }
)
def search_investments(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin_or_user),
    investor_id: Optional[uuid.UUID] = Query(None, description="Filter by the investor who made the investment."),
    min_amount: Optional[int] = Query(None, description="Filter for investments with an amount greater than or equal to this value."),
    max_amount: Optional[int] = Query(None, description="Filter for investments with an amount less than or equal to this value."),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
):
    return investment_service.search(
        db,
        investor_id=investor_id,
        min_amount=min_amount,
        max_amount=max_amount,
        skip=skip,
        limit=limit
    )

