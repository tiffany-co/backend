from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.user import User, UserRole
from app.schema.user import UserCreate, UserPublic
from app.services.user import user_service

router = APIRouter()

# Dependency for requiring admin role
require_admin = deps.require_role([UserRole.ADMIN])

@router.post(
    "/", 
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)] # Secure this endpoint
)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
):
    """
    Create a new user. (Admin only)
    """
    user = user_service.create_user(db=db, user_in=user_in)
    return user

@router.get("/me", response_model=UserPublic)
def read_current_user(
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Get the profile of the currently authenticated user.
    """
    return current_user
