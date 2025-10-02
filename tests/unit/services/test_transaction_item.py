"""
Unit tests for isolated business logic within the TransactionItemService.
"""

from decimal import Decimal
from pydantic import BaseModel

from app.services.transaction_item import transaction_item_service

# Create a simple mock object to simulate the data structure
# that the _calculate_item_total_price function expects.
class MockTransactionItem(BaseModel):
    unit_price: int
    weight_count: Decimal
    ojrat: Decimal
    profit: Decimal
    tax: Decimal

def test_calculate_item_total_price_for_sell():
    """
    Tests the total price calculation for a SELL transaction item.
    Formula: ((unit_price * (1 + ojrat/100)) * (1 + profit/100)) * weight_count
             + ((((unit_price * (1 + ojrat/100)) * (1 + profit/100)) - unit_price) * weight_count * tax/100)
    """
    # 1. Define the input data
    mock_item = MockTransactionItem(
        unit_price=1000,
        weight_count=Decimal("2.0"),
        ojrat=Decimal("10.0"),  # 10%
        profit=Decimal("5.0"),  # 5%
        tax=Decimal("9.0"),     # 9%
    )

    # Calculation breakdown:
    # wage_per_unit = 1000 * 0.10 = 100
    # price_after_wage = 1000 + 100 = 1100
    # profit_per_unit = 1100 * 0.05 = 55
    # price_after_profit = 1100 + 55 = 1155
    # gross_price = 1155 * 2 = 2310
    # net_price = 1000 * 2 = 2000
    # tax_amount = (2310 - 2000) * 0.09 = 310 * 0.09 = 27.9
    # total_price = 2310 + 27.9 = 2337.9
    # Expected result (as integer) = 2337
    expected_total = 2337

    # 2. Call the private method we want to test
    calculated_total = transaction_item_service._calculate_item_total_price(item=mock_item)

    # 3. Assert that the result is correct
    assert calculated_total == expected_total

def test_calculate_item_total_price_no_extras():
    """
    Tests the calculation when ojrat, profit, and tax are zero.
    The total price should simply be unit_price * weight_count.
    """
    mock_item = MockTransactionItem(
        unit_price=500,
        weight_count=Decimal("10.0"),
        ojrat=Decimal("0.0"),
        profit=Decimal("0.0"),
        tax=Decimal("0.0"),
    )
    expected_total = 5000  # 500 * 10

    calculated_total = transaction_item_service._calculate_item_total_price(item=mock_item)

    assert calculated_total == expected_total
