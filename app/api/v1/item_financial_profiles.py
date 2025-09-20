from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
import uuid

from app.api import deps
from app.models.user import User, UserRole
from app.schema.item_financial_profile import ItemFinancialProfileUpdate
from app.schema.item import ItemWithProfilesPublic
from app.schema.error import ErrorDetail
from app.services.item_financial_profile import item_financial_profile_service

router = APIRouter()

@router.put(
    "/{profile_id}",
    response_model=ItemWithProfilesPublic,
    summary="[Admin] Update a Financial Profile",
    description="Allows an administrator to update the default financial values for a specific item profile. The full parent item is returned upon success.",
    responses={
        200: {
            "description": "Financial profile updated successfully. Returns the full parent item.",
        },
        401: {"model": ErrorDetail, "description": "Unauthorized"},
        403: {"model": ErrorDetail, "description": "Forbidden"},
        404: {"model": ErrorDetail, "description": "Financial profile not found"},
    }
)
def update_item_financial_profile(
    profile_id: uuid.UUID,
    profile_in: ItemFinancialProfileUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
):
    updated_profile = item_financial_profile_service.update(db=db, profile_id=profile_id, profile_in=profile_in)
    return updated_profile.item
