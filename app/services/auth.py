from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.repository.user import user_repo
from app.core.security import verify_password
from app.models.user import User

class AuthService:
    """
    Service layer for handling authentication logic.
    """

    def authenticate_user(self, db: Session, *, form_data: OAuth2PasswordRequestForm) -> User:
        """
        Authenticates a user based on username and password from form data.

        Args:
            db: The database session.
            form_data: The OAuth2 form data containing username and password.

        Returns:
            The authenticated user object.

        Raises:
            HTTPException: If authentication fails.
        """
        user = user_repo.get_by_username(db, username=form_data.username)

        # Create a generic exception to avoid telling an attacker whether the username or password was wrong.
        auth_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

        if not user or not verify_password(form_data.password, user.hashed_password):
            raise auth_exception
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

        return user

# Create a single, importable instance of the AuthService
auth_service = AuthService()

