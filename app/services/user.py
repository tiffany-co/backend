from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import uuid
from app.models.user import User
from app.repository.user import user_repo
from app.schema.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

class UserService:
    """
    Service layer for user-related business logic.
    """

    def create_user(self, db: Session, *, user_in: UserCreate) -> User:
        """
        Handles the business logic for creating a new user.
        """
        if user_repo.get_by_username(db, username=user_in.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this username already exists.",
            )
        if user_repo.get_by_phone_number(db, phone_number=user_in.phone_number):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this phone number already exists.",
            )

        # Create a dictionary with the data to be stored in the database
        user_data_for_db = user_in.model_dump()
        user_data_for_db["hashed_password"] = get_password_hash(user_in.password)
        del user_data_for_db["password"] # Remove the plaintext password
        
        # Pass the clean dictionary to the repository
        db_user = user_repo.create(db, obj_in=user_data_for_db)
        return db_user

    def update_user(self, db: Session, *, user_obj: User, user_in: UserUpdate) -> User:
        """
        Handles the business logic for updating a user.
        """
        # Check for duplicate phone number if it's being changed
        if user_in.phone_number and user_in.phone_number != user_obj.phone_number:
            existing_phone = user_repo.get_by_phone_number(db, phone_number=user_in.phone_number)
            if existing_phone and existing_phone.id != user_obj.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This phone number is already registered.",
                )
        
        update_data = user_in.model_dump(exclude_unset=True)

        # Hash the new password if it's provided
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data["password"])
            del update_data["password"]

        return user_repo.update(db, db_obj=user_obj, obj_in=update_data)


# Create a single, importable instance of the UserService.
user_service = UserService()

