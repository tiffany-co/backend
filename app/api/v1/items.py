from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.api import deps
from app.models.user import UserRole
from app.schema.item import ItemCreate, ItemPublic, ItemUpdate
from app.services.item import item_service
from app.repository.item import item_repo

router = APIRouter()

# Dependency for requiring admin role
require_admin = deps.require_role([UserRole.ADMIN])

@router.post(
    "/",
    response_model=ItemPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
def create_item(*, db: Session = Depends(deps.get_db), item_in: ItemCreate):
    """
    Create a new item. (Admin only)
    """
    return item_service.create(db=db, obj_in=item_in)

@router.get("/", response_model=List[ItemPublic])
def read_all_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(deps.get_current_active_user),
):
    """
    Retrieve all items. (All authenticated users)
    """
    return item_repo.get_multi(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=ItemPublic)
def read_item_by_id(
    item_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_active_user),
):
    """
    Retrieve a specific item by its ID. (All authenticated users)
    """
    item = item_repo.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item

@router.put(
    "/{item_id}",
    response_model=ItemPublic,
    dependencies=[Depends(require_admin)],
)
def update_item(
    item_id: uuid.UUID,
    item_in: ItemUpdate,
    db: Session = Depends(deps.get_db),
):
    """
    Update an item. (Admin only)
    """
    item = item_repo.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item_service.update(db=db, db_obj=item, obj_in=item_in)

@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_item(
    item_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
):
    """
    Delete an item. (Admin only)
    """
    item = item_repo.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    item_repo.remove(db, id=item_id)
    return
