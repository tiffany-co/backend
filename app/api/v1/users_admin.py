from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from typing import List

from app.api import deps
from app.schema.user import UserCreate, UserPublic, UserUpdate
from app.services.user import user_service
from app.models.enums.user import UserRole
from app.repository.user import user_repo

router = APIRouter()

@router.post(
    "/",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Allows an administrator to create a new user with the 'USER' role.",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
    responses={
        201: {
            "description": "User created successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                        "username": "newuser",
                        "full_name": "New User",
                        "phone_number": "1122334455",
                        "is_active": True,
                        "role": "USER",
                        "created_at": "2025-09-02T12:00:00Z",
                        "updated_at": "2025-09-02T12:00:00Z"
                    }
                }
            }
        },
        400: {"description": "Bad Request (e.g., username or phone already exists)"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden (user is not an admin)"},
    }
)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
):
    """
    Admin endpoint to create a new user.
    """
    user = user_service.create_user(db=db, user_in=user_in)
    return user

@router.get(
    "/",
    response_model=List[UserPublic],
    summary="Get all users",
    description="Allows an administrator to retrieve a list of all users in the system.",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
)
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Admin endpoint to retrieve all users.
    """
    users = user_repo.get_multi(db, skip=skip, limit=limit)
    return users


@router.get(
    "/{user_id}",
    response_model=UserPublic,
    summary="Get user by ID",
    description="Allows an administrator to fetch a single user by their unique ID.",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
    responses={
        200: {"description": "Successful Response"},
        404: {"description": "User not found"},
    }
)
def read_user_by_id(
    user_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
):
    """
    Admin endpoint to get a specific user by their ID.
    """
    user = user_service.get_user_by_id(db, user_id=user_id)
    return user


@router.put(
    "/{user_id}",
    response_model=UserPublic,
    summary="Update a user",
    description="Allows an administrator to update a non-admin user's information.",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
    responses={
        200: {"description": "Successful Response"},
        400: {"description": "Bad Request (e.g., cannot update an admin)"},
        404: {"description": "User not found"},
    }
)
def update_user_by_id(
    *,
    db: Session = Depends(deps.get_db),
    user_id: uuid.UUID,
    user_in: UserUpdate,
):
    """
    Admin endpoint to update a user's details.
    """
    user_to_update = user_service.get_user_by_id(db, user_id=user_id)
    updated_user = user_service.update_user(db=db, user_obj=user_to_update, user_in=user_in)
    return updated_user


@router.delete(
    "/{user_id}",
    response_model=UserPublic,
    summary="Delete a user",
    description="Allows an administrator to delete a non-admin user.",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
     responses={
        200: {"description": "User deleted successfully"},
        400: {"description": "Bad Request (e.g., cannot delete an admin)"},
        404: {"description": "User not found"},
    }
)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: uuid.UUID,
):
    """
    Admin endpoint to delete a user.
    """
    user_to_delete = user_service.get_user_by_id(db, user_id=user_id)
    deleted_user = user_service.delete_user(db=db, user_obj=user_to_delete)
    return deleted_user
