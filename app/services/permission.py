from sqlalchemy.orm import Session
from typing import List
import uuid

from app.models.user import User, UserRole
from app.models.permission import Permission
from app.models.enums.permission import PermissionName
from app.repository.permission import permission_repo
from app.services.user import user_service
from app.logging_config import audit_logger, logger
from app.core.exceptions import AppException
from fastapi import status

class PermissionService:
    """
    Service layer for permission-related business logic.
    """

    def seed_permissions(self, db: Session):
        """
        Ensures all permissions from the PermissionName enum exist in the database.
        This is intended to be run on application startup.
        """
        existing_permissions_names = [p.name for p in permission_repo.get_multi(db)]
        all_permission_names = [p.value for p in PermissionName]
        
        missing_permissions = set(all_permission_names) - set(existing_permissions_names)

        if not missing_permissions:
            logger.info("All permissions are already in the database.")
            return

        for name in missing_permissions:
            permission_repo.create(db, obj_in={"name": name})
            logger.info(f"Created missing permission: {name}")

    def get_all_permissions(self, db: Session) -> List[Permission]:
        """Get a list of all available permissions."""
        return permission_repo.get_multi(db)

    def add_permission_to_user(self, db: Session, *, user_id: uuid.UUID, permission_name: PermissionName, current_user: User) -> User:
        """Adds a specific permission to a user."""
        user_to_update = user_service.get_user_by_id(db, user_id=user_id)
        permission_to_add = permission_repo.get_by_name(db, name=permission_name)

        if user_to_update.role == UserRole.ADMIN:
            raise AppException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot modify the permissions of an admin user.",
            )

        if not permission_to_add:
             raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Permission '{permission_name.value}' not found.",
            )

        if permission_to_add in user_to_update.permissions:
            raise AppException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User already has the permission '{permission_name.value}'.",
            )
        
        user_to_update.permissions.append(permission_to_add)
        db.commit()
        db.refresh(user_to_update)
        audit_logger.info(f"Permission '{permission_name.value}' added to user '{user_to_update.username}' by '{current_user.username}'.")
        return user_to_update
    
    def remove_permission_from_user(self, db: Session, *, user_id: uuid.UUID, permission_name: PermissionName, current_user: User) -> User:
        """Removes a specific permission from a user."""
        user_to_update = user_service.get_user_by_id(db, user_id=user_id)
        permission_to_remove = permission_repo.get_by_name(db, name=permission_name)

        if user_to_update.role == UserRole.ADMIN:
            raise AppException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot modify the permissions of an admin user.",
            )

        if not permission_to_remove:
             raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Permission '{permission_name.value}' not found.",
            )

        if permission_to_remove not in user_to_update.permissions:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User does not have the permission '{permission_name.value}'.",
            )
            
        user_to_update.permissions.remove(permission_to_remove)
        db.commit()
        db.refresh(user_to_update)
        audit_logger.info(f"Permission '{permission_name.value}' removed from user '{user_to_update.username}' by '{current_user.username}'.")
        return user_to_update

permission_service = PermissionService()

