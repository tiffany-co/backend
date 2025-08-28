from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.db.session import SessionLocal
from app.core.config import settings
from app.schema.token import TokenPayload
from app.models.user import User
from app.repository.user import user_repo

# Define the OAuth2 scheme.
# tokenUrl points to the endpoint where the client can get a token (our login endpoint).
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_db() -> Generator:
    """
    A dependency that provides a database session for a single request.
    It ensures the session is properly closed after the request is finished.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    """
    A dependency to get the current user from a JWT token.
    It decodes the token, validates its payload, and fetches the user from the DB.

    :param db: The database session.
    :param token: The JWT token from the request's Authorization header.
    :return: The authenticated User model instance.
    :raises HTTPException: If the token is invalid, expired, or the user doesn't exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = user_repo.get(db, id=token_data.sub)
    if not user:
        raise credentials_exception
    return user
