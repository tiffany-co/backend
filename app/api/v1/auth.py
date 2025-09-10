from datetime import timedelta
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core import security
from app.core.config import settings
from app.schema.token import Token
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
    OAuth2 compatible token login, get an access token for future requests.
    
    Takes a username and password from a form body.
    - Authenticates the user.
    - Creates and returns a JWT access token if successful.
    """
    user = auth_service.authenticate_user(db, form_data=form_data)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

