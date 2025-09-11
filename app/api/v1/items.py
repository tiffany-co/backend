from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
import uuid
from typing import List

from app.api import deps
from app.models.user import User, UserRole
from app.schema.item import ItemPublic, ItemUpdate
from app.schema.error import ErrorDetail
from app.services.item import item_service

router = APIRouter()

@router.get(
    "/",
    response_model=List[ItemPublic],
    summary="Get All Item Templates",
    description="Allows any authenticated user to retrieve a paginated list of all item templates.",
     responses={
        200: {"description": "A list of item templates."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
    }
)
def read_all_items(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
):
    return item_service.get_all(db, skip=skip, limit=limit)


@router.get(
    "/{item_id}",
    response_model=ItemPublic,
    summary="Get Item Template by ID",
    description="Allows any authenticated user to fetch a single item template by its ID.",
     responses={
        200: {"description": "The requested item template."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
        404: {"model": ErrorDetail, "description": "Item template not found"},
    }
)
def read_item_by_id(
    item_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return item_service.get_by_id(db, item_id=item_id)


@router.put(
    "/{item_id}",
    response_model=ItemPublic,
    summary="[Admin] Update Item Template",
    description="Allows an administrator to update an item template's defaults.",
    responses={
        200: {"description": "Item template updated successfully."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
        403: {"model": ErrorDetail, "description": "Forbidden"},
        404: {"model": ErrorDetail, "description": "Item template not found"},
        409: {"model": ErrorDetail, "description": "Conflict (e.g., name already exists)"},
    }
)
def update_item(
    item_id: uuid.UUID,
    item_in: ItemUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
):
    return item_service.update(db=db, item_id=item_id, item_in=item_in, current_user=current_user)

