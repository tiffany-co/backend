from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.schema.permission import PermissionPublic
from app.services.permission import permission_service
from app.schema.error import ErrorDetail
from app.models.user import User

router = APIRouter()

@router.get(
    "/",
    response_model=List[PermissionPublic],
    summary="Get All Available Permissions",
    description="Fetches a paginated list of all permissions that can be assigned to users.",
    responses={
        200: {
            "description": "A list of all available permissions.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                            "created_at": "2025-09-02T12:00:00Z",
                            "updated_at": "2025-09-02T12:00:00Z",
                            "name": "contact_update_all",
                            "name_fa": "ویرایش تمام مخاطبین",
                            "description_fa": "این دسترسی به کاربر اجازه می‌دهد تا اطلاعات تمام مخاطبین را ویرایش کند."
                        }
                    ]
                }
            }
        },
        401: {"model": ErrorDetail, "description": "Unauthorized"},
    }
)
def get_all_permissions(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0, description="Number of permissions to skip"),
    limit: int = Query(100, ge=1, le=200, description="Number of permissions to return"),
):
    """
    Public endpoint to retrieve a list of all possible permissions in the system.
    """
    return permission_service.get_all_permissions(db)

