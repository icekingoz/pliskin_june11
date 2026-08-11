import pytest

from pages.InventoryPage import InventoryPage


# Level 1 check: does the page load and can we see the button?
# Stays on inventory_page — this test needs an EMPTY cart.
def test_cart_page_loads(inventory_page: InventoryPage):
    cart_page = inventory_page.open_cart()

    assert cart_page.get_title().text_content() == "Your Cart"
    assert cart_page.get_checkout_button().is_visible()


# Parametrize + factory: the test data drives the cart_with call.
@pytest.mark.parametrize(
    "item_id, item_name",
    [
        ("sauce-labs-backpack", "Sauce Labs Backpack"),
        ("sauce-labs-bike-light", "Sauce Labs Bike Light"),
        ("sauce-labs-bolt-t-shirt", "Sauce Labs Bolt T-Shirt"),
        ("sauce-labs-onesie", "Sauce Labs Onesie"),
    ],
)
def test_each_product_can_be_added(cart_with, item_id, item_name):
    cart_page = cart_with(item_id)

    assert cart_page.get_item_count() == 1
    assert item_name in cart_page.get_item_names()


# Assignment 1: add two, check both names, remove one, count is 1.
def test_remove_one_item_from_cart(cart_with):
    cart_page = cart_with("sauce-labs-backpack", "sauce-labs-bike-light")

    # Both products are in the cart
    assert cart_page.get_item_count() == 2
    names = cart_page.get_item_names()
    assert "Sauce Labs Backpack" in names
    assert "Sauce Labs Bike Light" in names

    # Remove one of them
    cart_page.remove_item("sauce-labs-backpack")

    assert cart_page.get_item_count() == 1
    assert cart_page.get_item_names() == ["Sauce Labs Bike Light"]


# remove_item returns self, so calls can be chained. End state: cart empty.
def test_remove_both_items_by_chaining(cart_with):
    cart_page = cart_with("sauce-labs-backpack", "sauce-labs-bike-light")
    cart_page.remove_item("sauce-labs-backpack").remove_item("sauce-labs-bike-light")

    assert cart_page.get_item_count() == 0


# Assignment 4: logout. CartPage.logout() imports LoginPage inside the method,
# which is how we avoid the circular import between the page files.
def test_logout_from_cart(inventory_page: InventoryPage):
    cart_page = inventory_page.open_cart()
    login_page_again = cart_page.logout()

    # Back on the login screen: the credentials box is on show again.
    assert login_page_again.get_login_credentials().is_visible()
