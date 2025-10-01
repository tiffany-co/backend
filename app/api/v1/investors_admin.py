import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User, UserRole
from app.models.enums.investor import InvestorStatus
from app.schema.investor import InvestorCreate, InvestorUpdate, InvestorPublic
from app.schema.error import ErrorDetail
from app.services.investor import investor_service

router = APIRouter()

@router.post(
    "/",
    response_model=InvestorPublic,
    status_code=status.HTTP_201_CREATED,
    summary="[Admin] Create an Investor",
    description="Creates a new **Contact**, a new **User** with the 'INVESTOR' role, and links them via a new **Investor** profile.",
    responses={
        201: {"description": "Investor created successfully."},
        401: {"model": ErrorDetail, "description": "Unauthorized."},
        403: {"model": ErrorDetail, "description": "User does not have admin privileges."},
        409: {"model": ErrorDetail, "description": "Conflict. A user with the same username or contact with the same phone/national number already exists."},
    }
)
def create_investor(
    investor_in: InvestorCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
):
    """Creates a complete investor entity, including their user and contact details."""
    return investor_service.create(db, investor_in=investor_in, current_user=current_user)

@router.get(
    "/search",
    response_model=List[InvestorPublic],
    summary="Search Investors",
    description="Searches and filters all investor profiles. Open to any authenticated user.",
    responses={
        200: {"description": "A list of investors matching the criteria."},
        401: {"model": ErrorDetail, "description": "Unauthorized."},
    }
)
def search_investors(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin_or_user),
    first_name: Optional[str] = Query(None, description="Filter by first name (partial, case-insensitive)."),
    last_name: Optional[str] = Query(None, description="Filter by last name (partial, case-insensitive)."),
    national_number: Optional[str] = Query(None, description="Filter by exact national number."),
    phone_number: Optional[str] = Query(None, description="Filter by exact phone number."),
    username: Optional[str] = Query(None, description="Filter by username (partial, case-insensitive)."),
    status: Optional[InvestorStatus] = Query(None, description="Filter by investor account status."),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
):
    """Searches for investors based on their profile and contact information."""
    return investor_service.search(
        db, 
        first_name=first_name, 
        last_name=last_name, 
        national_number=national_number,
        phone_number=phone_number,
        username=username,
        status=status, 
        skip=skip, 
        limit=limit
    )

@router.get(
    "/{investor_id}",
    response_model=InvestorPublic,
    summary="Get Investor by ID",
    description="Retrieves a single investor's public profile. Open to any authenticated user.",
    responses={
        200: {"description": "The requested investor profile."},
        401: {"model": ErrorDetail, "description": "Unauthorized."},
        404: {"model": ErrorDetail, "description": "Investor not found."},
    }
)
def get_investor_by_id(
    investor_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin_or_user),
):
    """Get a single investor's profile by their unique investor ID."""
    return investor_service.get_by_id(db, investor_id=investor_id)


@router.put(
    "/{investor_id}",
    response_model=InvestorPublic,
    summary="[Admin] Update Investor Status",
    description="Updates an investor's status. Setting the status to 'CLOSED' will deactivate the associated user account, preventing login. Changing it back will reactivate them.",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
    responses={
        200: {"description": "Investor status updated successfully."},
        401: {"model": ErrorDetail, "description": "Unauthorized."},
        403: {"model": ErrorDetail, "description": "User does not have admin privileges."},
        404: {"model": ErrorDetail, "description": "Investor not found."},
    }
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
    description="Permanently deletes an investor, along with their associated user and contact info. Fails if the investor has any financial history (investments or approved payments).",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
    responses={
        204: {"description": "Investor deleted successfully."},
        400: {"model": ErrorDetail, "description": "Investor cannot be deleted due to existing financial history."},
        401: {"model": ErrorDetail, "description": "Unauthorized."},
        403: {"model": ErrorDetail, "description": "User does not have admin privileges."},
        404: {"model": ErrorDetail, "description": "Investor not found."},
    }
)
def delete_investor(
    investor_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
):
    """Deletes an investor, along with their associated user and contact info."""
    investor_service.delete(db, investor_id=investor_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

