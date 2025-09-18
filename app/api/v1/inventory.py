# app/api/v1/inventories.py
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Any, Dict

from app.api import deps
from app.models.user import User, UserRole
from app.schema.inventory import (
    InventoryHistoryPublic,
    InventoryBalanceResponse,
    InventoryAdjust,
)
from app.schema.error import ErrorDetail
from app.services.inventory import inventory_service

router = APIRouter()

@router.get(
    "/history",
    response_model=List[InventoryHistoryPublic],
    response_model_by_alias=False,  # Explicitly return programmatic keys
    summary="Get Inventory History",
    description="[Admin Only] Retrieves a paginated history of all inventory snapshots, newest first.",
)
def get_inventory_history(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination."),
    limit: int = Query(100, ge=1, le=200, description="Maximum number of records to return."),
) -> Any:
    """Retrieves a paginated history of all inventory snapshots, including metadata."""
    return inventory_service.get_all_history(db, skip=skip, limit=limit)

@router.get(
    "/balance",
    response_model=InventoryBalanceResponse,
    response_model_by_alias=False,  # Explicitly return programmatic keys
    summary="Get Current Inventory Balance",
    description="Retrieves the latest inventory balance with programmatic keys (e.g., 'new_gold').",
)
def get_current_balance(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
) -> Any:
    """Retrieves the latest inventory balance with standard English keys."""
    return inventory_service.get_current_balance(db)

@router.get(
    "/balance-fa",
    response_model=InventoryBalanceResponse,  # Use the unified response model
    response_model_by_alias=True,  # This is the key to activating the Persian aliases
    summary="Get Current Inventory Balance (Persian)",
    description="Retrieves the latest inventory balance with user-friendly Persian keys (e.g., 'طلای نو').",
    responses={
        200: {
            "description": "The current inventory balance with Persian keys.",
            "content": {
                "application/json": {
                    "example": {
                        "money_balance": 150000000,
                        "inventory": {
                            "طلای نو": 105.50,
                            "طلای مستعمل": 250.75,
                            "سکه پارسیان": 120.00,
                            "طلای آبشده": 500.00,
                            "زعفران": 30.00,
                            "دلار": 5000.00,
                            "یورو": 2500.00,
                            "پوند": 1000.00,
                            "سکه امامی ۸۶": 50,
                            "نیم سکه ۸۶": 100,
                            "ربع سکه ۸۶": 200,
                            "سکه امامی غیر": 15,
                            "نیم سکه غیر": 30,
                            "ربع سکه غیر": 45
                        }
                    }
                }
            }
        },
        401: {"model": ErrorDetail},
        403: {"model": ErrorDetail},
    }
)
def get_current_balance_fa(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
) -> Any:
    """Retrieves the latest inventory balance with Persian keys for display purposes."""
    return inventory_service.get_current_balance(db)

@router.post(
    "/adjust",
    response_model=InventoryHistoryPublic,
    response_model_by_alias=False,  # Explicitly return programmatic keys
    status_code=status.HTTP_201_CREATED,
    summary="Manually Adjust Inventory",
    description="[Admin Only] Creates a new inventory snapshot with manually adjusted values.",
)
def adjust_inventory(
    adjustment_in: InventoryAdjust,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([UserRole.ADMIN])),
) -> Any:
    """
    Allows an administrator to make a manual adjustment to the inventory.
    This creates a new snapshot with the updated values and returns the new record.
    """
    return inventory_service.adjust_inventory(
        db=db, adjustment_in=adjustment_in, current_user=current_user
    )

