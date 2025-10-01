import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User, UserRole
from app.models.enums.investor import InvestorStatus
from app.schema.investor import InvestorCreate, InvestorUpdate, InvestorPublic
from app.services.investor import investor_service

router = APIRouter()

@router.post(
    "/",
    response_model=InvestorPublic,
    status_code=status.HTTP_201_CREATED,
    summary="[Admin] Create an Investor",
)
def create_investor(
    investor_in: InvestorCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
):
    """Creates a new Contact, User (as investor), and Investor profile."""
    return investor_service.create(db, investor_in=investor_in, current_user=current_user)

@router.get(
    "/search",
    response_model=List[InvestorPublic],
    summary="Search Investors",
)
def search_investors(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    national_number: Optional[str] = Query(None),
    phone_number: Optional[str] = Query(None),
    status: Optional[InvestorStatus] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
):
    """Search for investors. Open to all authenticated users."""
    return investor_service.search(
        db, 
        first_name=first_name, 
        last_name=last_name, 
        national_number=national_number,
        phone_number=phone_number,
        status=status, 
        skip=skip, 
        limit=limit
    )

@router.get(
    "/{investor_id}",
    response_model=InvestorPublic,
    summary="Get Investor by ID",
)
def get_investor_by_id(
    investor_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """Get a single investor's profile. Open to all authenticated users."""
    return investor_service.get_by_id(db, investor_id=investor_id)


@router.put(
    "/{investor_id}",
    response_model=InvestorPublic,
    summary="[Admin] Update Investor Status",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
)
def update_investor(
    investor_id: uuid.UUID,
    investor_in: InvestorUpdate,
    db: Session = Depends(deps.get_db),
):
    """Update an investor's status (e.g., to suspend or close their account)."""
    return investor_service.update(db, investor_id=investor_id, investor_in=investor_in)


@router.delete(
    "/{investor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="[Admin] Delete an Investor",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
)
def delete_investor(
    investor_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
):
    """Deletes an investor, along with their associated user and contact info."""
    investor_service.delete(db, investor_id=investor_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
