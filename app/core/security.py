import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Any, Union

from jose import jwt
from app.core.config import settings

ALGORITHM = "HS256"


def _create_token(
    subject: Union[str, Any],
    expires_delta: timedelta,
    secret_key: str,
) -> str:
    """
    Internal helper to create a JWT.
    """
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def create_access_token(
    subject: Union[str, Any],
) -> str:
    """
    Creates a new JWT access token.
    """
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_token(subject, expires_delta, settings.SECRET_KEY)


def create_refresh_token(
    subject: Union[str, Any]
) -> str:
    """
    Creates a new JWT refresh token.
    """
    expires_delta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    return _create_token(subject, expires_delta, settings.REFRESH_TOKEN_SECRET_KEY)


def verify_value(plain_value: str, hashed_value: str) -> bool:
    """
    Verifies a plain value against a hashed value using bcrypt.
    """
    return bcrypt.checkpw(plain_value.encode('utf-8'), hashed_value.encode('utf-8'))


def get_hashed_value(value: str) -> str:
    """
    Hashes a value using bcrypt.
    """
    hashed_bytes = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')

