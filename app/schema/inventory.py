from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Optional
from decimal import Decimal
import uuid

from .base import BaseSchema

# --- A single, reusable schema for all inventory items ---
# This schema is the single source of truth for both programmatic keys and their Persian aliases.
class InventoryItemsSchema(BaseModel):
    """A detailed breakdown of all inventoried items."""
    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    new_gold: Decimal = Field(0, description="Balance of New Gold (grams, 2 decimal places)", serialization_alias="طلای نو")
    used_gold: Decimal = Field(0, description="Balance of Used Gold (grams, 2 decimal places)", serialization_alias="طلای مستعمل")
    persian_coin: Decimal = Field(0, description="Balance of Persian Coins (weight, grams, 2 decimal places)", serialization_alias="سکه پارسیان")
    molten_gold: Decimal = Field(0, description="Balance of Molten Gold (grams, 2 decimal places)", serialization_alias="طلای آبشده")
    saffron: Decimal = Field(0, description="Balance of Saffron (grams, 2 decimal places)", serialization_alias="زعفران")
    dollar: Decimal = Field(0, description="Balance of US Dollars (2 decimal places)", serialization_alias="دلار")
    euro: Decimal = Field(0, description="Balance of Euros (2 decimal places)", serialization_alias="یورو")
    pound: Decimal = Field(0, description="Balance of British Pounds (2 decimal places)", serialization_alias="پوند")
    
    emami_coin_86: int = Field(0, description="Count of Emami Coins (1386)", serialization_alias="سکه امامی ۸۶")
    half_coin_86: int = Field(0, description="Count of Half Coins (1386)", serialization_alias="نیم سکه ۸۶")
    quarter_coin_86: int = Field(0, description="Count of Quarter Coins (1386)", serialization_alias="ربع سکه ۸۶")
    emami_coin_etc: int = Field(0, description="Count of other Emami Coins", serialization_alias="سکه امامی غیر")
    half_coin_etc: int = Field(0, description="Count of other Half Coins", serialization_alias="نیم سکه غیر")
    quarter_coin_etc: int = Field(0, description="Count of other Quarter Coins", serialization_alias="ربع سکه غیر")

# --- API Response Schemas ---

class InventoryPublic(BaseModel):
    """Base schema for displaying an inventory snapshot."""
    description: Optional[str] = None
    transaction_id: Optional[uuid.UUID] = None
    payment_id: Optional[uuid.UUID] = None
    money_balance: int = Field(..., description="Cash balance in Iranian Rials.")
    inventory: InventoryItemsSchema

class InventoryHistoryPublic(InventoryPublic, BaseSchema):
    """Schema for a single inventory snapshot in the history, including all metadata."""
    pass

class InventoryBalanceResponse(BaseModel):
    """Unified response schema for the current inventory balance."""
    money_balance: int
    inventory: InventoryItemsSchema

# --- API Input Schema ---

class InventoryAdjust(BaseModel):
    """Schema for making a manual adjustment to the inventory."""
    description: Optional[str] = Field(None, description="An optional note explaining the reason for the manual adjustment.")
    money_balance: Optional[int] = Field(None, description="The new cash balance in Iranian Rials.")
    inventory: Optional[InventoryItemsSchema] = Field({}, description="An object containing the new balances for any items you want to adjust.")

    @model_validator(mode='after')
    def check_at_least_one_adjustment(self) -> 'InventoryAdjust':
        """Ensure that at least one field is being adjusted."""
        if self.money_balance is None and (not self.inventory or not self.inventory.model_dump(exclude_unset=True)):
            raise ValueError("At least one field (money_balance or an item in inventory) must be provided for adjustment.")
        return self

