from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import uuid
from typing import List

from app.core.exceptions import AppException
from app.models.user import User
from app.models.enums.user import UserRole
from app.repository.user import user_repo
from app.schema.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from app.logging_config import audit_logger

class UserService:
    """
    Service layer for user-related business logic.
    """

    def get_user_by_id(self, db: Session, *, user_id: uuid.UUID) -> User:
        """Helper method to get a user by ID or raise a 404 exception."""
        user = user_repo.get(db, id=user_id)
        if not user:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found.",
            )
        return user

    def get_user_by_username(self, db: Session, *, username: str) -> User:
        """Helper method to get a user by username or raise a 404 exception."""
        user = user_repo.get_by_username(db, username=username)
        if not user:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with username '{username}' not found.",
            )
        return user
    
    def get_all_users(self, db: Session, skip: int, limit: int) -> List[User]:
        """Get all users from the database."""
        return user_repo.get_multi(db, skip=skip, limit=limit)

    def create_user(self, db: Session, *, user_in: UserCreate) -> User:
        """
        Handles the business logic for creating a new user.
        New users are always created with the 'USER' role by default.
        """
        if user_repo.get_by_username(db, username=user_in.username):
            raise AppException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this username already exists.",
            )
        if user_repo.get_by_phone_number(db, phone_number=user_in.phone_number):
            raise AppException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this phone number already exists.",
            )

        user_data_for_db = user_in.model_dump()
        user_data_for_db["hashed_password"] = get_password_hash(user_in.password)
        user_data_for_db["role"] = UserRole.USER
        del user_data_for_db["password"]
        
        db_user = user_repo.create(db, obj_in=user_data_for_db)
        audit_logger.info(f"User '{db_user.username}' (ID: {db_user.id}) created.")
        return db_user

    def update_user(
        self, db: Session, *, user_to_update: User, user_in: UserUpdate, current_user: User
    ) -> User:
        """
        Handles the business logic for updating a user with permission checks.
        """
        if user_to_update.role == UserRole.ADMIN and user_to_update.id != current_user.id:
            raise AppException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admins cannot update other admins.",
            )

        if user_in.is_active is False and user_to_update.id == current_user.id:
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Users cannot deactivate themselves.",
            )
            
        if user_in.username and user_in.username != user_to_update.username:
            existing_user = user_repo.get_by_username(db, username=user_in.username)
            if existing_user and existing_user.id != user_to_update.id:
                raise AppException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This username is already registered.",
                )
                
        if user_in.phone_number and user_in.phone_number != user_to_update.phone_number:
            existing_phone = user_repo.get_by_phone_number(db, phone_number=user_in.phone_number)
            if existing_phone and existing_phone.id != user_to_update.id:
                raise AppException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This phone number is already registered.",
                )
        
        update_data = user_in.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data["password"])
            del update_data["password"]

        updated_user = user_repo.update(db, db_obj=user_to_update, obj_in=update_data)
        audit_logger.info(f"User '{updated_user.username}' (ID: {updated_user.id}) updated by User '{current_user.username}'.")
        return updated_user

    def delete_user(self, db: Session, *, user_id: uuid.UUID, current_user: User) -> User:
        """
        Handles the business logic for deleting a user with permission checks.
        """
        user_to_delete = self.get_user_by_id(db, user_id=user_id)

        if user_to_delete.role == UserRole.ADMIN:
            raise AppException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admins cannot be deleted.",
            )
        
        if user_to_delete.id == current_user.id:
             raise AppException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Users cannot delete themselves.",
            )

        deleted_user = user_repo.remove(db, id=user_id)
        audit_logger.info(f"User '{deleted_user.username}' (ID: {deleted_user.id}) deleted by User '{current_user.username}'.")
        return deleted_user

user_service = UserService()

