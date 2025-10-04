from fastapi import APIRouter, Depends, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.schema.token import Token, TokenRefreshRequest
from app.services.auth import auth_service

router = APIRouter()

@router.post(
    "/login",
    response_model=Token,
    tags=["Authentication"],
    summary="Create Access & Refresh Tokens",
    description="Logs in a user and returns a JWT access and refresh token.",
    responses={
        status.HTTP_200_OK: {
            "description": "Successful Login",
            "content": {
                "application/json": {
                    "examples": {
                        "Success": {
                            "summary": "Successful Login",
                            "value": {
                                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                                "token_type": "bearer"
                            }
                        }
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "User is inactive",
            "content": {
                "application/json": {
                    "examples": {
                        "inactive_user": {
                            "summary": "Inactive User",
                            "value": {"detail": "Inactive user"}
                        }
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect username or password",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_credentials": {
                            "summary": "Invalid Credentials",
                            "value": {"detail": "Incorrect username or password"}
                        }
                    }
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
    """
    _, access_token, refresh_token = auth_service.handle_login(db=db, form_data=form_data)
    
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
    token_in: TokenRefreshRequest = Body(..., examples={
            "normal": {
                "summary": "A normal example",
                "description": "A normal example of a refresh token.",
                "value": {"refresh_token": "abcd"},
            }
        },
    ),
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

