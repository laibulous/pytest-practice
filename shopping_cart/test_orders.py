import pytest
from shopping_cart.orders import Order, Item, calculate_total

@pytest.mark.parametrize("subtotal, shipping, discount, tax_percent,expected",[
    (12, 5, 2, 0.1, 16.5),
    (0, 0, 0, 0, 0),
    (100, 10, 20, 0.2, 108),
    (50, 5, 60, 0.1, 0),
])
def test_calculate_total_normal(subtotal, shipping, discount, tax_percent,expected):
    result = calculate_total(subtotal, shipping, discount, tax_percent)
    assert result == expected

@pytest.mark.parametrize("subtotal, shipping, discount, tax_percent, expected_error", [
    (-12, 5, 2, 0.1,"subtotal cannot be negative"),
    (0, -10, 0, 0, "shipping cannot be negative"),
    (100, 10, 20, -1.2, "tax_percent cannot be negative"),
    (50, 5, -6, 0.1, "discount cannot be negative"),])
def test_calculate_total_with_negative_values(subtotal, shipping, discount, tax_percent, expected_error):
    with pytest.raises(ValueError, match=expected_error):
        calculate_total(subtotal, shipping, discount, tax_percent)

def test_calculate_total_rounding():
    result = calculate_total(10.1234, 0, 0, 0)
    assert result == 10.12
