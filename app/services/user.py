from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.repository.user import user_repo
from app.schema.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

class UserService:
    """
    Service layer for user-related business logic.
    It orchestrates the repository and other components to perform user operations.
    """

    def create_user(self, db: Session, *, user_in: UserCreate) -> User:
        """
        Handles the business logic for creating a new user.

        - Checks for existing username or phone number.
        - Hashes the password.
        - Calls the repository to create the user in the database.

        :param db: The database session.
        :param user_in: The Pydantic schema containing the new user's data.
        :return: The newly created User model instance.
        :raises HTTPException: If the username or phone number is already registered.
        """
        # Check if a user with the same username already exists
        existing_user = user_repo.get_by_username(db, username=user_in.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this username already exists.",
            )

        # Check if a user with the same phone number already exists
        existing_phone = user_repo.get_by_phone_number(db, phone_number=user_in.phone_number)
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this phone number already exists.",
            )

        # Hash the password before storing it
        hashed_password = get_password_hash(user_in.password)
        
        # Create a dictionary for the new user data, replacing the plain password
        user_data = user_in.model_dump()
        user_data['hashed_password'] = hashed_password
        del user_data['password'] # Remove the plain password

        # Create the user using the repository
        db_user = user_repo.create(db, obj_in=user_data)
        return db_user

# Create a single, importable instance of the UserService.
user_service = UserService()
