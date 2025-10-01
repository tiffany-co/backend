from typing import List
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schema.investor import InvestorProfilePublic, InvestorPasswordUpdate
from app.schema.investment import InvestmentPublic
from app.schema.payment import PaymentPublic
from app.schema.error import ErrorDetail
from app.services.user import user_service
from app.services.payment import payment_service

router = APIRouter()

@router.get(
    "/me",
    response_model=InvestorProfilePublic,
    summary="[Investor] Get My Profile",
    description="Fetches the profile, credit, and status for the currently logged-in investor.",
    responses={
        200: {"description": "The investor's profile."},
        401: {"model": ErrorDetail, "description": "Unauthorized."},
        403: {"model": ErrorDetail, "description": "User is not an investor."},
    }
)
def get_my_profile(
    current_user: User = Depends(deps.get_current_active_investor)
):
    """Fetches the profile, credit, and status for the currently logged-in investor."""
    return current_user.investor_profile

@router.get(
    "/me/investments",
    response_model=List[InvestmentPublic],
    summary="[Investor] Get My Investments",
    description="Fetches a list of all investments made by the currently logged-in investor.",
    responses={
        200: {"description": "A list of the investor's investments."},
        401: {"model": ErrorDetail, "description": "Unauthorized."},
        403: {"model": ErrorDetail, "description": "User is not an investor."},
    }
)
def get_my_investments(
    current_user: User = Depends(deps.get_current_active_investor)
):
    """Fetches a list of all investments made by the currently logged-in investor."""
    return current_user.investor_profile.investments

@router.get(
    "/me/payments",
    response_model=List[PaymentPublic],
    summary="[Investor] Get My Payments",
    description="Fetches a list of all payments associated with the currently logged-in investor.",
    responses={
        200: {"description": "A list of the investor's payments."},
        401: {"model": ErrorDetail, "description": "Unauthorized."},
        403: {"model": ErrorDetail, "description": "User is not an investor."},
    }
)
def get_my_payments(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_investor),
):
    """Fetches a list of all payments associated with the currently logged-in investor."""
    return payment_service.search(db, current_user=current_user)

@router.put(
    "/me/password",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="[Investor] Update My Password",
    description="Allows the currently logged-in investor to change their own password.",
    responses={
        204: {"description": "Password updated successfully."},
        400: {"model": ErrorDetail, "description": "Incorrect current password."},
        401: {"model": ErrorDetail, "description": "Unauthorized."},
        403: {"model": ErrorDetail, "description": "User is not an investor."},
    }
)
def update_my_password(
    password_in: InvestorPasswordUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_investor),
):
    """Allows the currently logged-in investor to change their own password."""
    user_service.update_password(db, user=current_user, password_in=password_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

