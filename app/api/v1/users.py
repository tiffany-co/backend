from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.user import User
from app.schema.user import UserCreate, UserPublic
from app.services.user import user_service

router = APIRouter()

@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
    # TODO: Add dependency to check for admin privileges
    # current_user: User = Depends(deps.get_current_admin_user),
):
    """
    Create a new user.
    This endpoint should be restricted to admin users in a real application.
    """
    user = user_service.create_user(db=db, user_in=user_in)
    return user

@router.get("/me", response_model=UserPublic)
def read_current_user(
    current_user: User = Depends(deps.get_current_user),
):
    """
    Get the profile of the currently authenticated user.
    """
    return current_user
