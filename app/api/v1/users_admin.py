from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session
import uuid
from typing import List

from app.api import deps
from app.schema.user import UserCreate, UserPublic, UserUpdate, UserInList
from app.schema.permission import PermissionPublic, UserPermissionCreate
from app.schema.error import ErrorDetail
from app.services.user import user_service
from app.services.permission import permission_service
from app.models.enums.user import UserRole
from app.models.enums.permission import PermissionName
from app.models.user import User

router = APIRouter()

@router.post(
    "/",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create a New User (Admin Only)",
    description="Allows an administrator to create a new user with the default 'USER' role.",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
    responses={
        201: {
            "description": "User created successfully.",
            "content": {"application/json": {"example": {"id": "a1b2c3d4-e5f6-7890-1234-567890abcdef", "username": "newuser", "full_name": "New User", "phone_number": "1122334455", "is_active": True, "role": "USER", "created_at": "2025-09-02T12:00:00Z", "updated_at": "2025-09-02T12:00:00Z"}}},
        },
        401: {
            "description": "Unauthorized - The user is not authenticated.",
            "model": ErrorDetail,
            "content": {
                "application/json": {
                    "example": {"detail": "Not authenticated"}
                }
            }
        },
        403: {
            "description": "Forbidden - The user does not have the required admin role.",
            "model": ErrorDetail,
            "content": {
                "application/json": {
                    "example": {"detail": "You do not have permission to access this resource"}
                }
            }
        },
        409: {
            "description": "Conflict Error",
            "model": ErrorDetail,
            "content": {"application/json": {"examples": {
                "username_exists": {"summary": "Username already exists", "value": {"detail": "A user with this username already exists."}},
                "phone_exists": {"summary": "Phone number already exists", "value": {"detail": "A user with this phone number already exists."}}
            }}},
        }
    }
)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
):
    """Admin endpoint to create a new user."""
    user = user_service.create_user(db=db, user_in=user_in)
    return user

@router.get(
    "/",
    response_model=List[UserInList],
    summary="Get All Users (Admin Only)",
    description="Allows an administrator to retrieve a paginated list of all users.",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
    responses={
        401: {
            "description": "Unauthorized - The user is not authenticated.",
            "model": ErrorDetail,
            "content": {
                "application/json": {
                    "example": {"detail": "Not authenticated"}
                }
            }
        },
        403: {
            "description": "Forbidden - The user does not have the required admin role.",
            "model": ErrorDetail,
            "content": {
                "application/json": {
                    "example": {"detail": "You do not have permission to access this resource"}
                }
            }
        }
    }
)
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=200, description="Number of users to return"),
):
    """Admin endpoint to retrieve all users."""
    users = user_service.get_all_users(db, skip=skip, limit=limit)
    return users

@router.get(
    "/id/{user_id}",
    response_model=UserPublic,
    summary="Get User by ID (Admin Only)",
    description="Allows an administrator to fetch a single user by their unique ID.",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
    responses={
        200: {
            "description": "Successful Response",
            "content": {"application/json": {"example": {"id": "a1b2c3d4-e5f6-7890-1234-567890abcdef", "username": "existinguser", "full_name": "Existing User", "phone_number": "5544332211", "is_active": True, "role": "USER", "created_at": "2025-09-01T10:00:00Z", "updated_at": "2025-09-01T10:00:00Z"}}},
        },
        404: {"description": "User not found", "model": ErrorDetail, "content": {"application/json": {"example": {"detail": "User not found"}}}},
        403: {
            "description": "Forbidden - The user does not have the required admin role.",
            "model": ErrorDetail,
            "content": {
                "application/json": {
                    "example": {"detail": "You do not have permission to access this resource"}
                }
            }
        }
    }
)
def read_user_by_id(
    user_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
):
    """Admin endpoint to get a specific user by their ID."""
    user = user_service.get_user_by_id(db=db, user_id=user_id)
    return user

@router.get(
    "/username/{username}",
    response_model=UserPublic,
    summary="Get User by Username (Admin Only)",
    description="Allows an administrator to fetch a single user by their username.",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
    responses={
        200: {
            "description": "Successful Response",
            "content": {"application/json": {"example": {"id": "a1b2c3d4-e5f6-7890-1234-567890abcdef", "username": "existinguser", "full_name": "Existing User", "phone_number": "5544332211", "is_active": True, "role": "USER", "created_at": "2025-09-01T10:00:00Z", "updated_at": "2025-09-01T10:00:00Z"}}},
        },
        404: {"description": "User not found", "model": ErrorDetail, "content": {"application/json": {"example": {"detail": "User not found"}}}},
        403: {
            "description": "Forbidden - The user does not have the required admin role.",
            "model": ErrorDetail,
            "content": {
                "application/json": {
                    "example": {"detail": "You do not have permission to access this resource"}
                }
            }
        }
    }
)
def read_user_by_username(
    username: str,
    db: Session = Depends(deps.get_db),
):
    """Admin endpoint to get a specific user by their username."""
    user = user_service.get_user_by_username(db=db, username=username)
    return user

@router.put(
    "/{user_id}",
    response_model=UserPublic,
    summary="Update a User (Admin Only)",
    description="Allows an administrator to update a non-admin user's information.",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
    responses={
        200: {"description": "Successful Response", "model": ErrorDetail},
        403: {"description": "Forbidden", "model": ErrorDetail, "content": {"application/json": {"example": {"detail": "Admins cannot update other admins."}}}},
        404: {"description": "User not found", "model": ErrorDetail},
        409: {"description": "Conflict Error", "model": ErrorDetail},
    }
)
def update_user_by_id(
    *,
    db: Session = Depends(deps.get_db),
    user_id: uuid.UUID,
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_active_user)
):
    """Admin endpoint to update a user's details."""
    user_to_update = user_service.get_user_by_id(db=db, user_id=user_id)
    updated_user = user_service.update_user(db=db, user_to_update=user_to_update, user_in=user_in, current_user=current_user)
    return updated_user

@router.delete(
    "/{user_id}",
    response_model=UserPublic,
    summary="Delete a User (Admin Only)",
    description="Allows an administrator to delete a non-admin user.",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
     responses={
        200: {"description": "User deleted successfully"},
        403: {"description": "Forbidden", "model": ErrorDetail, "content": {"application/json": {"examples": {
            "delete_admin": {"summary": "Cannot delete admin", "value": {"detail": "Admins cannot be deleted."}},
            "delete_self": {"summary": "Cannot delete self", "value": {"detail": "Users cannot delete themselves."}}
        }}}},
        404: {"description": "User not found", "model": ErrorDetail},
    }
)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user)
):
    """Admin endpoint to delete a user."""
    deleted_user = user_service.delete_user(db=db, user_id=user_id, current_user=current_user)
    return deleted_user

@router.get(
    "/{user_id}/permissions",
    response_model=List[PermissionPublic],
    summary="Get a User's Permissions (Admin Only)",
    description="Fetches a list of all permissions assigned to a specific user.",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
    responses={
        200: {"description": "A list of the user's permissions."},
        401: {"description": "Unauthorized", "model": ErrorDetail, "content": {"application/json": {"example": {"detail": "Not authenticated"}}}},
        403: {"description": "Forbidden", "model": ErrorDetail, "content": {"application/json": {"example": {"detail": "The user does not have enough privileges"}}}},
        404: {"description": "User not found", "model": ErrorDetail, "content": {"application/json": {"example": {"detail": "User with ID ... not found."}}}},
    }
)
def get_user_permissions(user_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    user = user_service.get_user_by_id(db=db, user_id=user_id)
    return user.permissions

@router.post(
    "/{user_id}/permissions",
    response_model=UserPublic,
    summary="Add a Permission to a User (Admin Only)",
    description="Assigns a new permission to a specific user.",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
    responses={
        200: {
            "description": "Permission added successfully. Returns the user's new list of all permissions.",
            "content": {"application/json": {"example": [{"id": "a1b2c3d4...", "name": "contact_update_all", "created_at": "...", "updated_at": "..."}]}}
        },
        401: {"description": "Unauthorized", "model": ErrorDetail, "content": {"application/json": {"example": {"detail": "Not authenticated"}}}},
        403: {"description": "Forbidden", "model": ErrorDetail, "content": {"application/json": {"example": {"detail": "Cannot modify the permissions of an admin user."}}}},
        404: {"description": "User or Permission not found", "model": ErrorDetail, "content": {"application/json": {"example": {"detail": "Permission 'some_permission' not found."}}}},
        409: {"description": "Conflict - User already has permission", "model": ErrorDetail, "content": {"application/json": {"example": {"detail": "User already has the permission 'contact_update_all'."}}}},
    }
)
def add_permission_to_user(
    user_id: uuid.UUID,
    permission_in: UserPermissionCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    user = permission_service.add_permission_to_user(
        db=db, 
        user_id=user_id, 
        permission_name=permission_in.permission_name, 
        current_user=current_user
    )
    return user

@router.delete(
    "/{user_id}/permissions/{permission_name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a Permission from a User (Admin Only)",
    description="Removes a specific permission from a user.",
    dependencies=[Depends(deps.require_role([UserRole.ADMIN]))],
    responses={
        204: {"description": "Permission removed successfully. No content is returned."},
        401: {"description": "Unauthorized", "model": ErrorDetail, "content": {"application/json": {"example": {"detail": "Not authenticated"}}}},
        403: {"description": "Forbidden", "model": ErrorDetail, "content": {"application/json": {"example": {"detail": "Cannot modify the permissions of an admin user."}}}},
        404: {"description": "User or Permission not found", "model": ErrorDetail, "content": {"application/json": {"example": {"detail": "User does not have the permission 'contact_update_all'."}}}},
    }
)
def remove_permission_from_user(
    user_id: uuid.UUID,
    permission_name: PermissionName,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    permission_service.remove_permission_from_user(
        db=db,
        user_id=user_id,
        permission_name=permission_name,
        current_user=current_user
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
