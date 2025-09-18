from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.models.user import User, UserRole
from app.schema.inventory import InventoryPublic, InventoryBalanceResponse, InventoryAdjust
from app.schema.error import ErrorDetail
from app.services.inventory import inventory_service

router = APIRouter()

@router.get(
    "/history",
    response_model=List[InventoryPublic],
    summary="Get Inventory History",
    description="[Admin Only] Retrieves a paginated history of all inventory snapshots.",
    responses={
        200: {
            "description": "A list of inventory snapshots in a nested format.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                            "created_at": "2025-09-15T10:00:00Z",
                            "updated_at": "2025-09-15T10:00:00Z",
                            "description": "Initial inventory setup",
                            "money_balance": 50000000,
                            "inventory": {
                                "new_gold": 100.50,
                                "emami_coin_86": 10,
                                # ... other item balances ...
                            }
                        }
                    ]
                }
            }
        },
        401: {"model": ErrorDetail, "description": "Unauthorized"},
        403: {"model": ErrorDetail, "description": "Forbidden"},
    }
)
def get_inventory_history(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
):
    return inventory_service.get_all_history(db, skip=skip, limit=limit)


@router.get(
    "/balance",
    response_model=InventoryBalanceResponse,
    summary="Get Current Inventory Balance",
    description="Retrieves the latest inventory balance with programmatic keys (e.g., 'new_gold', 'emami_coin_86').",
    responses={
        200: {"description": "The current inventory balance."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
    }
)
def get_current_balance(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return inventory_service.get_current_balance(db)


@router.get(
    "/balance-fa",
    response_model=InventoryBalanceResponse,
    summary="Get Current Inventory Balance (Persian)",
    description="Retrieves the latest inventory balance with user-friendly Persian keys (e.g., 'طلای نو').",
     responses={
        200: {"description": "The current inventory balance with Persian keys."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
    }
)
def get_current_balance_fa(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return inventory_service.get_current_balance_fa(db)


@router.post(
    "/adjust",
    response_model=InventoryPublic,
    status_code=status.HTTP_201_CREATED,
    summary="[Admin] Manually Adjust Inventory",
    description="Allows an administrator to make a manual adjustment to the inventory. This creates a new snapshot with the updated values.",
    responses={
        201: {"description": "Inventory adjusted successfully. Returns the new snapshot."},
        422: {"description": "Validation Error (e.g., invalid item name or empty adjustment)."},
        401: {"model": ErrorDetail, "description": "Unauthorized"},
        403: {"model": ErrorDetail, "description": "Forbidden"},
    }
)
def adjust_inventory(
    adjustment_in: InventoryAdjust,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
):
    return inventory_service.adjust_inventory(db=db, adjustment_in=adjustment_in, current_user=current_user)

