from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Dict, Optional, Any
from decimal import Decimal
import uuid
from datetime import datetime

from .base import BaseSchema
from ..models.inventory import Inventory # Import for the validator

# --- A reusable schema for the itemized inventory fields ---
# This schema provides detailed documentation for each field that will appear in Swagger.
class InventoryItemsSchema(BaseModel):
    new_gold: Optional[Decimal] = Field(None, description="Balance of New Gold (in grams, to 2 decimal places)")
    used_gold: Optional[Decimal] = Field(None, description="Balance of Used Gold (in grams, to 2 decimal places)")
    persian_coin: Optional[Decimal] = Field(None, description="Balance of Persian Coins (by weight, in grams, to 2 decimal places)")
    molten_gold: Optional[Decimal] = Field(None, description="Balance of Molten Gold (in grams, to 2 decimal places)")
    saffron: Optional[Decimal] = Field(None, description="Balance of Saffron (in grams, to 2 decimal places)")
    dollar: Optional[Decimal] = Field(None, description="Balance of US Dollars (to 2 decimal places)")
    euro: Optional[Decimal] = Field(None, description="Balance of Euros (to 2 decimal places)")
    pound: Optional[Decimal] = Field(None, description="Balance of British Pounds (to 2 decimal places)")
    
    emami_coin_86: Optional[int] = Field(None, description="Count of Emami Coins (1386)")
    half_coin_86: Optional[int] = Field(None, description="Count of Half Coins (1386)")
    quarter_coin_86: Optional[int] = Field(None, description="Count of Quarter Coins (1386)")
    emami_coin_etc: Optional[int] = Field(None, description="Count of other Emami Coins")
    half_coin_etc: Optional[int] = Field(None, description="Count of other Half Coins")
    quarter_coin_etc: Optional[int] = Field(None, description="Count of other Quarter Coins")

class InventoryPublic(BaseSchema):
    """Schema for a single, detailed inventory snapshot, including timestamps."""
    description: Optional[str] = None
    money_balance: int = Field(..., description="Cash balance in Iranian Rials.")
    inventory: InventoryItemsSchema
    
    # This validator transforms the flat database model into the nested structure for the API.
    @model_validator(mode='before')
    @classmethod
    def assemble_nested_inventory(cls, data: Any) -> Any:
        if isinstance(data, Inventory):
            inventory_data = {key: getattr(data, key) for key in InventoryItemsSchema.model_fields.keys() if hasattr(data, key)}
            return {
                **model_to_dict(data), # Helper to get base fields
                'inventory': inventory_data
            }
        return data

    class Config:
        from_attributes = True

class InventoryBalanceResponse(BaseModel):
    """Schema for the current inventory balance, using a nested structure."""
    money_balance: int = Field(..., description="Cash balance in Iranian Rials.")
    inventory: InventoryItemsSchema

class InventoryAdjust(BaseModel):
    """
    Schema for making a manual adjustment to the inventory.
    Uses a consistent nested structure.
    """
    description: str = Field(..., min_length=10, description="A required note explaining the reason for the manual adjustment.")
    money_balance: Optional[int] = Field(None, description="The new cash balance in Iranian Rials.")
    inventory: Optional[InventoryItemsSchema] = Field({}, description="An object containing the new balances for the items you want to adjust.")

    @model_validator(mode='before')
    @classmethod
    def check_at_least_one_adjustment(cls, data: Any) -> Any:
        """Ensures that at least one field is being adjusted."""
        if isinstance(data, dict):
            money_balance = data.get('money_balance')
            inventory_adjustments = data.get('inventory', {})
            
            if money_balance is None and not inventory_adjustments:
                raise ValueError("At least one field (money_balance or an inventory item) must be provided for adjustment.")
        return data

# Helper function for the validator
def model_to_dict(obj: Any) -> Dict[str, Any]:
    """A simplified helper to convert model to dict for the validator."""
    return {
        'id': obj.id,
        'created_at': obj.created_at,
        'updated_at': obj.updated_at,
        'description': obj.description,
        'money_balance': obj.money_balance,
    }

