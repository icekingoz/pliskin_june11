import pytest
from playwright.sync_api import Page

from pages.LoginPage import LoginPage


# TEMPORARY HELPER
# Adding a product to the cart happens on the INVENTORY page, so really this
# belongs on InventoryPage as add_item_to_cart(item_id). Until that method
# exists, we keep it here in ONE place so there is only one line to move later.
def add_item_to_cart(page: Page, item_id: str):
    # item_id looks like "sauce-labs-backpack"
    page.locator(f"[data-test=\"add-to-cart-{item_id}\"]").click()


# Level 1 check: does the page load and can we see the button?
def test_cart_page_loads(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    inventory_page = login_page.login_standard_user()

    cart_page = inventory_page.open_cart()

    assert cart_page.get_title().text_content() == "Your Cart"
    assert cart_page.get_checkout_button().is_visible()


# Standard example: one product, one clear story.
def test_added_item_appears_in_cart(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    inventory_page = login_page.login_standard_user()

    add_item_to_cart(page, "sauce-labs-backpack")
    cart_page = inventory_page.open_cart()

    assert cart_page.get_item_count() == 1
    assert cart_page.get_item_names() == ["Sauce Labs Backpack"]


# Parameterized example: same steps, four different products.
# pytest runs this test once per row, so one test becomes four.
@pytest.mark.parametrize(
    "item_id, item_name",
    [
        ("sauce-labs-backpack", "Sauce Labs Backpack"),
        ("sauce-labs-bike-light", "Sauce Labs Bike Light"),
        ("sauce-labs-bolt-t-shirt", "Sauce Labs Bolt T-Shirt"),
        ("sauce-labs-onesie", "Sauce Labs Onesie"),
    ],
)
def test_each_product_can_be_added(page: Page, item_id, item_name):
    login_page = LoginPage(page)
    login_page.open()
    inventory_page = login_page.login_standard_user()

    add_item_to_cart(page, item_id)
    cart_page = inventory_page.open_cart()

    assert cart_page.get_item_count() == 1
    assert item_name in cart_page.get_item_names()


# Assignment 1: add two, check both names, remove one, count is 1.
def test_remove_one_item_from_cart(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    inventory_page = login_page.login_standard_user()

    add_item_to_cart(page, "sauce-labs-backpack")
    add_item_to_cart(page, "sauce-labs-bike-light")

    cart_page = inventory_page.open_cart()

    # Both products are in the cart
    assert cart_page.get_item_count() == 2
    names = cart_page.get_item_names()
    assert "Sauce Labs Backpack" in names
    assert "Sauce Labs Bike Light" in names

    # Remove one of them
    cart_page.remove_item("sauce-labs-backpack")

    assert cart_page.get_item_count() == 1
    assert cart_page.get_item_names() == ["Sauce Labs Bike Light"]


# remove_item returns self, so calls can be chained.
def test_remove_both_items_by_chaining(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    inventory_page = login_page.login_standard_user()

    add_item_to_cart(page, "sauce-labs-backpack")
    add_item_to_cart(page, "sauce-labs-bike-light")

    cart_page = inventory_page.open_cart()
    cart_page.remove_item("sauce-labs-backpack").remove_item("sauce-labs-bike-light")

    assert cart_page.get_item_count() == 0


# Assignment 4: logout. CartPage.logout() imports LoginPage inside the method,
# which is how we avoid the circular import between the page files.
def test_logout_from_cart(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    inventory_page = login_page.login_standard_user()

    cart_page = inventory_page.open_cart()
    login_page_again = cart_page.logout()

    # Back on the login screen: the credentials box is on show again.
    assert login_page_again.get_login_credentials().is_visible()
