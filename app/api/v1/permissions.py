from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.schema.permission import PermissionPublic
from app.services.permission import permission_service

router = APIRouter()

@router.get(
    "/",
    response_model=List[PermissionPublic],
    summary="Get All Available Permissions",
    description="Fetches a list of all permissions that can be assigned to users.",
    responses={
        200: {
            "description": "A list of all available permissions.",
            "content": {
                "application/json": {
                    "example": [
                        {"id": "a1b2c3d4-e5f6-7890-1234-567890abcdef", "name": "contact_update_all"}
                    ]
                }
            }
        }
    }
)
def get_all_permissions(db: Session = Depends(deps.get_db)):
    """
    Public endpoint to retrieve a list of all possible permissions in the system.
    """
    return permission_service.get_all_permissions(db)
