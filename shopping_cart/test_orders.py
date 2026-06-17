import pytest
from shopping_cart.orders import Order, Item, calculate_total

@pytest.fixture
def pencil():
    return Item("Pencil", 0.5, 2)
@pytest.fixture
def order_one():
    order=Order(shipping=5, discount=2, tax_percent=0.1)
    return order
@pytest.fixture
def simple_items():
    item1 = Item("Marker", 1.5, 1)
    item2 = Item("Notebook", 2.5, 3)
    item3 = Item("Eraser", 0.75, 4)
    return [item1, item2, item3]


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

@pytest.mark.item
def test_create_item():
    item = Item("Book", 12.99, 2)
    assert item.name == "Book"
    assert item.unit_price == 12.99
    assert item.quantity == 2

@pytest.mark.item
def test_create_single_item():
    item = Item("Pen", 1.5)
    assert item.name == "Pen"
    assert item.unit_price == 1.5
    assert item.quantity == 1

@pytest.mark.item
def test_create_item_with_zero_quantity():
    item = Item("Pencil", 0.5, 0)
    assert item.calculate_item_total() == 0

@pytest.mark.item
def test_calculate_item_total(pencil):
    total = pencil.calculate_item_total()
    assert total == 1.0

@pytest.mark.item
def test_calculate_item_total_rounding():
    item = Item("Gadget", 19.999, 1)
    total = item.calculate_item_total()
    assert total == 20.00 

@pytest.mark.orders
def test_create_order():
    order = Order(shipping=5, discount=2, tax_percent=0.1)
    assert order.shipping == 5
    assert order.discount == 2
    assert order.tax_percent == 0.1
    assert order.items == []

@pytest.mark.orders
def test_create_empty_order():
    order = Order()
    assert order.shipping == 0
    assert order.discount == 0
    assert order.tax_percent == 0
    assert order.calculate_subtotal() == 0

@pytest.mark.orders
def test_add_item_to_order(order_one, pencil):
    order_one.add_item(pencil)
    order_one.add_item(Item("Marker", 1.5, 1))
    assert len(order_one.items) == 2
    assert order_one.items[0] == pencil    

@pytest.mark.orders
def test_calculate_subtotal_with_one_item(order_one, pencil):
    order_one.add_item(pencil)
    subtotal = order_one.calculate_subtotal()
    assert subtotal == 1.0

@pytest.mark.orders
def test_calculate_subtotal_with_multiple_items(order_one, simple_items):
    for item in simple_items:
        order_one.add_item(item)
    subtotal = order_one.calculate_subtotal()
    assert subtotal == 12

@pytest.mark.orders
def test_calculate_order_total(order_one, simple_items):
    for item in simple_items:
        order_one.add_item(item)
    total = order_one.calculate_order_total()
    assert total == 16.5

@pytest.mark.orders
def test_calculate_empty_order_total():
    order=Order()
    total = order.calculate_order_total()
    assert total == 0

@pytest.mark.orders
def test_get_reward_points_for_order_total_above_threshold(order_one):
    item1 = Item("Marker", 1.5, 1000)
    item2 = Item("Notebook", 2.5, 3000)
    item3 = Item("Eraser", 0.75, 4000)
    order_one.add_item(item1)
    order_one.add_item(item2)
    order_one.add_item(item3)
    reward=order_one.get_reward_points()
    assert reward == 13213

@pytest.mark.orders
def test_get_reward_points_for_order_total_below_threshold(order_one, simple_items):
    for item in simple_items:
        order_one.add_item(item)
    reward=order_one.get_reward_points()
    assert reward == 16

def test_get_reward_points_for_empty_order(order_one):
    reward = order_one.get_reward_points()
    assert reward == 3

def test_get_reward_points_for_order_total_exactly_at_threshold(order_one):
    item1 = Item("Marker", 3, 102.16)
    item2 = Item("Notebook", 4, 100)
    item3 = Item("Eraser", 2, 100)
    order_one.add_item(item1)
    order_one.add_item(item2)
    order_one.add_item(item3)
    reward=order_one.get_reward_points()
    assert reward == 1010
