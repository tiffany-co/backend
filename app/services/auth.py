from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError

from app.repository.user import user_repo
from app.core.security import verify_password, get_password_hash
from app.models.user import User
from app.core.config import settings
from app.schema.token import TokenPayload

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


    def refresh_token(self, db: Session, *, refresh_token: str) -> tuple[str, str]:
        """
        Refreshes an access token using a rotating refresh token.

        Args:
            db: The database session.
            refresh_token: The refresh token to use.

        Returns:
            A tuple containing the new access token and new refresh token.

        Raises:
            HTTPException: If the refresh token is invalid or expired.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials, please log in again",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                refresh_token, settings.REFRESH_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
        except JWTError:
            raise credentials_exception

        user = user_repo.get(db, id=token_data.sub)

        # 1. Check if user exists and has a stored refresh token
        if not user or not user.hashed_refresh_token:
            raise credentials_exception

        # 2. Compare the provided token with the stored hash
        if not verify_password(refresh_token, user.hashed_refresh_token):
            # This is a critical security event. The refresh token might have been stolen and reused.
            # Invalidate all current refresh tokens for this user.
            user.hashed_refresh_token = None
            db.commit()
            raise credentials_exception

        # 3. If validation is successful, issue a new pair of tokens
        from app.core import security
        new_access_token = security.create_access_token(subject=user.id)
        new_refresh_token = security.create_refresh_token(subject=user.id)

        # 4. Store the hash of the new refresh token, invalidating the old one
        user.hashed_refresh_token = get_password_hash(new_refresh_token)
        db.add(user)
        db.commit()

        return new_access_token, new_refresh_token

# Create a single, importable instance of the AuthService
auth_service = AuthService()

