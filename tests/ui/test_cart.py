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


def test_add_three_items_and_remove_one(cart_with):
    cart_page = cart_with(
        "sauce-labs-backpack",
        "sauce-labs-bike-light",
        "sauce-labs-bolt-t-shirt",
    )

    assert cart_page.get_item_count() == 3
    assert cart_page.get_item_names() == [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
        "Sauce Labs Bolt T-Shirt",
    ]

    cart_page.remove_item("sauce-labs-bike-light")

    assert cart_page.get_item_count() == 2
    assert cart_page.get_item_names() == [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt",
    ]


# remove_item returns self, so calls can be chained. End state: cart empty.
def test_remove_both_items_by_chaining(cart_with):
    cart_page = cart_with("sauce-labs-backpack", "sauce-labs-bike-light")
    cart_page.remove_item("sauce-labs-backpack").remove_item("sauce-labs-bike-light")

    assert cart_page.get_item_count() == 0
    assert cart_page.get_item_names() == []


def test_cart_badge_appears_when_item_added(cart_with):
    cart_page = cart_with("sauce-labs-backpack")
    assert cart_page.get_cart_badge().is_visible()


def test_remove_item_updates_cart_badge(cart_with):
    cart_page = cart_with("sauce-labs-backpack", "sauce-labs-bike-light")
    assert cart_page.get_cart_badge_count() == 2

    cart_page.remove_item("sauce-labs-backpack")
    assert cart_page.get_cart_badge_count() == 1
    assert cart_page.get_item_names() == ["Sauce Labs Bike Light"]

    cart_page.remove_item("sauce-labs-bike-light")
    assert cart_page.get_cart_badge_count() == 0
    assert cart_page.get_item_count() == 0


def test_logout_returns_to_login_screen(inventory_page: InventoryPage):
    login_page = inventory_page.open_cart().logout()

    assert login_page.login_button.is_visible()
    assert login_page.page.url.rstrip("/") == "https://www.saucedemo.com"


def test_logout_blocks_direct_inventory_access(inventory_page: InventoryPage):
    login_page = inventory_page.open_cart().logout()
    login_page.page.goto("/inventory.html")

    assert login_page.login_button.is_visible()
    assert login_page.get_error_message().text_content() == (
        "Epic sadface: You can only access '/inventory.html' when you are logged in."
    )
