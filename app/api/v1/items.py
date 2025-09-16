from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
import uuid
from typing import List

from app.api import deps
from app.models.user import User, UserRole
from app.schema.item import ItemUpdate, ItemInList, ItemInListWithProfiles, ItemWithProfilesPublic
from app.schema.error import ErrorDetail
from app.services.item import item_service

router = APIRouter()

@router.get(
    "/",
    response_model=List[ItemInList],
    summary="Get All Items",
    description="Allows any authenticated user to retrieve a list of all defined item types. This view excludes timestamps.",
    responses={
        200: {"description": "A list of items."},
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
    "/with-profiles",
    response_model=List[ItemInListWithProfiles],
    summary="Get All Items with Financial Profiles",
    description="Retrieves all items, with their nested financial profiles for buying and selling.",
    responses={
        200: {"description": "A list of items with their financial profiles."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
    }
)
def read_all_items_with_profiles(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return item_service.get_all(db, limit=1000)


@router.get(
    "/{item_id}",
    response_model=ItemWithProfilesPublic,
    summary="Get Item by ID",
    description="Allows any authenticated user to fetch a single item by its ID. This view includes timestamps.",
     responses={
        200: {"description": "The requested item."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
        404: {"model": ErrorDetail, "description": "Item not found"},
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
    response_model=ItemWithProfilesPublic,
    summary="[Admin] Update Item Metadata",
    description="Allows an administrator to update an item's metadata (e.g., Persian name, category, description).",
    responses={
        200: {"description": "Item updated successfully."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
        403: {"model": ErrorDetail, "description": "Forbidden"},
        404: {"model": ErrorDetail, "description": "Item not found"},
    }
)
def update_item(
    item_id: uuid.UUID,
    item_in: ItemUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
):
    return item_service.update(db=db, item_id=item_id, item_in=item_in, current_user=current_user)

