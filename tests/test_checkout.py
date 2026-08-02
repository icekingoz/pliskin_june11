import pytest
from playwright.sync_api import Page

from pages.LoginPage import LoginPage


# Same temporary helper as in test_cart.py — it belongs on InventoryPage later.
def add_item_to_cart(page: Page, item_id: str):
    page.locator(f"[data-test=\"add-to-cart-{item_id}\"]").click()


# Standard example: the full happy path, top to bottom.
# Read it out loud — login, add, open cart, check out, assert.
def test_checkout_happy_path(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    inventory_page = login_page.login_standard_user()

    add_item_to_cart(page, "sauce-labs-backpack")

    cart_page = inventory_page.open_cart()
    assert cart_page.get_item_count() == 1

    checkout_page = cart_page.start_checkout()
    checkout_page.fill_information("Solid", "Snake", "00001")

    # Step two: the overview still shows our product
    assert checkout_page.get_title().text_content() == "Checkout: Overview"
    assert checkout_page.get_item_names() == ["Sauce Labs Backpack"]

    checkout_page.finish()

    assert checkout_page.get_complete_header().text_content() == "Thank you for your order!"


# fill_information() and finish() both return self, so the steps can be chained.
def test_checkout_chained(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    inventory_page = login_page.login_standard_user()

    add_item_to_cart(page, "sauce-labs-bike-light")

    checkout_page = inventory_page.open_cart().start_checkout()
    checkout_page.fill_information("Solid", "Snake", "00001").finish()

    assert checkout_page.get_complete_header().text_content() == "Thank you for your order!"


# Parameterized example: the same flow with different customers.
@pytest.mark.parametrize(
    "first_name, last_name, postal_code",
    [
        ("Solid", "Snake", "00001"),
        ("Ada", "Lovelace", "SW1A 1AA"),
        ("Grace", "Hopper", "12345"),
        ("Alan", "Turing", "M1 1AE"),
    ],
)
def test_checkout_with_different_customers(page: Page, first_name, last_name, postal_code):
    login_page = LoginPage(page)
    login_page.open()
    inventory_page = login_page.login_standard_user()

    add_item_to_cart(page, "sauce-labs-backpack")

    checkout_page = inventory_page.open_cart().start_checkout()
    checkout_page.fill_information(first_name, last_name, postal_code).finish()

    assert checkout_page.get_complete_header().text_content() == "Thank you for your order!"


# Parameterized sad path: the SAME fill_information() method, but here we expect
# an error. The page object stays neutral; the test decides what "correct" means.
@pytest.mark.parametrize(
    "first_name, last_name, postal_code, error",
    [
        ("", "Snake", "00001", "Error: First Name is required"),
        ("Solid", "", "00001", "Error: Last Name is required"),
        ("Solid", "Snake", "", "Error: Postal Code is required"),
    ],
)
def test_checkout_form_requires_all_fields(page: Page, first_name, last_name, postal_code, error):
    login_page = LoginPage(page)
    login_page.open()
    inventory_page = login_page.login_standard_user()

    add_item_to_cart(page, "sauce-labs-backpack")

    checkout_page = inventory_page.open_cart().start_checkout()
    checkout_page.fill_information(first_name, last_name, postal_code)

    #                 expected  vs  actual
    assert error in checkout_page.get_error_message().text_content()
    # And we never left step one
    assert checkout_page.get_title().text_content() == "Checkout: Your Information"


# The overview totals: subtotal is the price of what we added.
def test_checkout_overview_subtotal(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    inventory_page = login_page.login_standard_user()

    add_item_to_cart(page, "sauce-labs-backpack")   # $29.99

    checkout_page = inventory_page.open_cart().start_checkout()
    checkout_page.fill_information("Solid", "Snake", "00001")

    assert checkout_page.get_subtotal() == 29.99
    # Total is subtotal plus tax, so it must be larger
    assert checkout_page.get_total() > checkout_page.get_subtotal()


# After ordering, "Back Home" returns us to the products page.
def test_back_home_after_order(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    inventory_page = login_page.login_standard_user()

    add_item_to_cart(page, "sauce-labs-backpack")

    checkout_page = inventory_page.open_cart().start_checkout()
    checkout_page.fill_information("Solid", "Snake", "00001").finish()

    inventory_page_again = checkout_page.back_home()

    assert inventory_page_again.get_title().text_content() == "Products"
