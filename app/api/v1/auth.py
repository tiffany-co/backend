from datetime import timedelta
from fastapi import APIRouter, Depends, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core import security
from app.core.config import settings
from app.schema.token import Token, TokenRefreshRequest
from app.services.auth import auth_service

router = APIRouter()

@router.post(
    "/login",
    response_model=Token,
    tags=["Authentication"],
    summary="Create Access Token",
    description="Logs in a user and returns a JWT access token.",
    responses={
        status.HTTP_200_OK: {
            "description": "Successful Login",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
                        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
                        "token_type": "bearer"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "User is inactive",
            "content": {
                "application/json": {
                    "example": {"detail": "Inactive user"}
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect username or password",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect username or password"}
                }
            },
            "headers": {
                "WWW-Authenticate": {
                    "schema": {
                        "type": "string"
                    },
                    "description": "Bearer"
                }
            }
        }
    }
)
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    """
    OAuth2 compatible token login, get access and refresh tokens.
    
    - Authenticates the user.
    - Creates and returns JWT tokens.
    - Stores a hash of the refresh token in the database for rotation.
    """
    user = auth_service.authenticate_user(db, form_data=form_data)
    
    access_token = security.create_access_token(subject=user.id)
    refresh_token = security.create_refresh_token(subject=user.id)

    # Store a hash of the refresh token to enable rotation
    user.hashed_refresh_token = security.get_password_hash(refresh_token)
    db.add(user)
    db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh Access Token",
    description="Get a new access and refresh token using a valid refresh token.",
    responses={
        status.HTTP_200_OK: {
            "description": "Token refreshed successfully"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        }
    }
)
def refresh_token(
    db: Session = Depends(deps.get_db),
    token_in: TokenRefreshRequest = Body(...),
) -> Token:
    """
    Get a new pair of tokens.
    """
    new_access_token, new_refresh_token = auth_service.refresh_token(
        db=db, refresh_token=token_in.refresh_token
    )
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }
