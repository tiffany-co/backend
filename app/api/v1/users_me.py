from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
import uuid

from app.api import deps
from app.schema.user import UserPublic, UserUpdate
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
    current_user: User = Depends(deps.get_current_active_user)
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
                        "is_active": True,
                        "role": "USER",
                        "created_at": "2025-09-02T10:30:00Z",
                        "updated_at": "2025-09-02T11:00:00Z"
                    }
                }
            }
        },
        400: {
            "description": "Bad Request (e.g., phone number or username already registered)",
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
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Update the profile of the currently logged-in user.
    """
    user = user_service.update_user(db=db, user_to_update=current_user, user_in=user_in, current_user=current_user)
    return user
