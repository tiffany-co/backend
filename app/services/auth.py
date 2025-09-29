from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError

from app.repository.user import user_repo
from app.core.security import verify_value, get_hashed_value, create_access_token, create_refresh_token
from app.models.user import User
from app.core.config import settings
from app.schema.token import TokenPayload, Token


class AuthService:
    """
    Service layer for handling authentication logic.
    """

    def authenticate_user(self, db: Session, *, form_data: OAuth2PasswordRequestForm) -> User:
        """
        Authenticates a user based on username and password from form data.
        """
        user = user_repo.get_by_username(db, username=form_data.username)

        auth_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

        if not user or not verify_value(form_data.password, user.hashed_password):
            raise auth_exception
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

        return user

    def handle_login(self, db: Session, *, form_data: OAuth2PasswordRequestForm) -> tuple[User, str, str]:
        """
        Handles the complete login flow: authentication, token creation, and refresh token storage.
        """
        user = self.authenticate_user(db, form_data=form_data)
        
        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)

        user.hashed_refresh_token = get_hashed_value(refresh_token)
        db.add(user)
        db.commit()
        
        return user, access_token, refresh_token

    def refresh_token(self, db: Session, *, refresh_token: str) -> tuple[str, str]:
        """
        Refreshes an access token using a rotating refresh token.
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

        if not user or not user.hashed_refresh_token:
            raise credentials_exception

        if not verify_value(refresh_token, user.hashed_refresh_token):
            user.hashed_refresh_token = None
            db.commit()
            raise credentials_exception

        new_access_token = create_access_token(subject=user.id)
        new_refresh_token = create_refresh_token(subject=user.id)

        user.hashed_refresh_token = get_hashed_value(new_refresh_token)
        db.add(user)
        db.commit()

        return new_access_token, new_refresh_token

auth_service = AuthService()

