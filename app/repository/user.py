from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schema.user import UserCreate, UserUpdate
from .base import BaseRepository

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """
    Repository for User model operations.
    Inherits from BaseRepository and adds user-specific query methods.
    """

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """
        Retrieves a user by their username.

        :param db: The database session.
        :param username: The username to search for.
        :return: The User instance if found, otherwise None.
        """
        return db.query(User).filter(User.username == username).first()

    def get_by_phone_number(self, db: Session, *, phone_number: str) -> Optional[User]:
        """
        Retrieves a user by their phone number.

        :param db: The database session.
        :param phone_number: The phone number to search for.
        :return: The User instance if found, otherwise None.
        """
        return db.query(User).filter(User.phone_number == phone_number).first()

# Create a single, importable instance of the UserRepository.
# This is often referred to as a singleton pattern, ensuring that we use the
# same repository instance throughout the application.
user_repo = UserRepository(User)
