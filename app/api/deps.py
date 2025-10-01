from typing import Generator, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.db.session import SessionLocal
from app.core.config import settings
from app.schema.token import TokenPayload
from app.models.user import User, UserRole
from app.models.permission import PermissionName
from app.repository.user import user_repo

# Define the OAuth2 scheme.
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_db() -> Generator:
    """
    Dependency to provide a database session per request.
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
    Dependency to get the current user from a JWT token.
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
    
    if token_data.sub is None:
        raise credentials_exception
        
    user = user_repo.get(db, id=token_data.sub)
    if not user:
        raise credentials_exception
    
    # Add the current user's ID to the session info dictionary
    # This makes it available to the SQLAlchemy event listeners for auditing.
    db.info['current_user_id'] = user.id
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency to get the current active user.
    Raises an exception if the user is inactive.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def require_role(required_roles: List[UserRole]):
    """
    A dependency factory that creates a dependency to check user roles.
    
    :param required_roles: A list of roles that are allowed to access the endpoint.
    """
    def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )
        return current_user
    return role_checker

def require_permission(required_permission: PermissionName):
    """
    A dependency factory that creates a dependency to check if a user has a specific permission.
    Admins are always granted access.
    """
    def permission_checker(current_user: User = Depends(get_current_active_user)) -> User:
        # Admins have all permissions implicitly
        if current_user.role == UserRole.ADMIN:
            return current_user
        
        # Check if the user has the required permission in their list
        user_permissions = {perm.name for perm in current_user.permissions}
        if required_permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You do not have the required permission: '{required_permission.value}'",
            )
        return current_user
    return permission_checker


# --- Role-specific dependency shortcuts ---
# Use these in your endpoints for cleaner, more readable authorization checks.

get_current_active_admin_or_user = require_role([UserRole.ADMIN, UserRole.USER])
get_current_active_investor = require_role([UserRole.INVESTOR])
