from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
import uuid
from typing import List

from app.api import deps
from app.schema.user import UserPublic, UserUpdateMe
from app.schema.permission import PermissionPublic
from app.schema.error import ErrorDetail
from app.services.user import user_service
from app.models.user import User

router = APIRouter()

@router.get(
    "/me",
    response_model=UserPublic,
    summary="Get Current User Profile",
    description="Fetches the complete profile information for the currently authenticated user.",
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                        "username": "johndoe",
                        "full_name": "John Doe",
                        "phone_number": "1234567890",
                        "is_active": True,
                        "role": "USER",
                        "created_at": "2025-09-02T10:30:00Z",
                        "updated_at": "2025-09-02T10:30:00Z"
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized",
            "model": ErrorDetail,
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authenticated"
                    }
                }
            }
        },
    }
)
def read_current_user(
    current_user: User = Depends(deps.get_current_active_admin_or_user)
):
    """
    Get the profile of the currently logged-in user.
    """
    return current_user


@router.put(
    "/me",
    response_model=UserPublic,
    summary="Update Current User Profile",
    description="Allows the currently authenticated user to update their own profile information.",
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                        "username": "new_johndoe",
                        "full_name": "Johnathan Doe",
                        "phone_number": "0987654321",
                        "role": "user",
                    }
                }
            }
        },
        400: {
            "description": "Bad Request (e.g., phone number or username already registered)",
            "model": ErrorDetail,
            "content": {
                "application/json": {
                    "example": {
                       "detail": "This username is already registered."
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized",
            "model": ErrorDetail,
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authenticated"
                    }
                }
            }
        }
    }
)
def update_current_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdateMe,
    current_user: User = Depends(deps.get_current_active_admin_or_user)
):
    """
    Update the profile of the currently logged-in user.
    """
    user = user_service.update_user(db=db, user_to_update=current_user, user_in=user_in, current_user=current_user)
    return user


@router.get(
    "/me/permissions",
    response_model=List[PermissionPublic],
    summary="Get Current User's Permissions",
    description="Fetches a list of all permissions assigned to the currently authenticated user.",
    responses={
        200: {
            "description": "A list of the user's assigned permissions.",
            "content": {
                "application/json": {
                    "example": [
                        {"id": "a1b2c3d4-e5f6-7890-1234-567890abcdef", "name": "contact_update_all"},
                    ]
                }
            }
        },
        401: {
            "description": "Unauthorized. The user is not authenticated.",
            "model": ErrorDetail,
            "content": {
                "application/json": {
                    "example": {"detail": "Not authenticated"}
                }
            }
        },
    }
)
def get_current_user_permissions(
    current_user: User = Depends(deps.get_current_active_admin_or_user)
):
    """Get the permissions of the currently logged-in user."""
    return current_user.permissions