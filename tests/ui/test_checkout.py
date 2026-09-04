import pytest

from pages.CheckoutPage import CheckoutPage


def test_checkout_happy(checkout_started: CheckoutPage):
    checkout_started.fill_information("Solid", "Snake", "00001")
    assert checkout_started.get_title().text_content() == "Checkout: Overview"
    #                  Returns a List
    assert checkout_started.get_item_names() == ["Sauce Labs Backpack"]

    checkout_started.finish()
    assert checkout_started.get_complete_header().text_content() == "Thank you for your order!"


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
def test_checkout_with_different_customers(
    checkout_started: CheckoutPage, first_name, last_name, postal_code
):
    checkout_started.fill_information(first_name, last_name, postal_code).finish()
    assert checkout_started.get_complete_header().text_content() == "Thank you for your order!"


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
def test_checkout_form_requires_all_fields(
    checkout_started: CheckoutPage, first_name, last_name, postal_code, error
):
    checkout_started.fill_information(first_name, last_name, postal_code)

    #                 expected  vs  actual
    assert error in checkout_started.get_error_message().text_content()
    # And we never left step one
    assert checkout_started.get_title().text_content() == "Checkout: Your Information"


# The overview totals: subtotal is the price of what we added ($29.99).
def test_checkout_overview_subtotal(checkout_started: CheckoutPage):
    checkout_started.fill_information("Solid", "Snake", "00001")

    assert checkout_started.get_subtotal() == 29.99
    # Total is subtotal plus tax, so it must be larger
    assert checkout_started.get_total() > checkout_started.get_subtotal()


# After ordering, "Back Home" returns us to the products page.
def test_back_home_after_order(completed_order: CheckoutPage):
    assert completed_order.back_home().get_title().text_content() == "Products"


# --- Boundary: checkout information form ---
# Validation is first-error-wins: first name, then last name, then postal code.

def test_checkout_empty_first_name_shows_its_own_error(checkout_started: CheckoutPage):
    checkout_started.fill_information("", "Snake", "00001")
    assert checkout_started.get_error_message().text_content() == "Error: First Name is required"
    assert checkout_started.get_title().text_content() == "Checkout: Your Information"


def test_checkout_empty_last_name_shows_its_own_error(checkout_started: CheckoutPage):
    checkout_started.fill_information("Solid", "", "00001")
    assert checkout_started.get_error_message().text_content() == "Error: Last Name is required"
    assert checkout_started.get_title().text_content() == "Checkout: Your Information"


def test_checkout_empty_postal_code_shows_its_own_error(checkout_started: CheckoutPage):
    checkout_started.fill_information("Solid", "Snake", "")
    assert checkout_started.get_error_message().text_content() == "Error: Postal Code is required"
    assert checkout_started.get_title().text_content() == "Checkout: Your Information"


def test_checkout_empty_first_and_last_name_shows_first_name_error(
    checkout_started: CheckoutPage,
):
    checkout_started.fill_information("", "", "00001")
    assert checkout_started.get_error_message().text_content() == "Error: First Name is required"
    assert checkout_started.get_title().text_content() == "Checkout: Your Information"


def test_checkout_all_three_fields_empty_shows_first_name_error(
    checkout_started: CheckoutPage,
):
    checkout_started.fill_information("", "", "")
    assert checkout_started.get_error_message().text_content() == "Error: First Name is required"
    assert checkout_started.get_title().text_content() == "Checkout: Your Information"


def test_checkout_accepts_200_character_values(checkout_started: CheckoutPage):
    long_value = "A" * 200
    checkout_started.fill_information(long_value, long_value, long_value)
    # TODO: confirm whether the app truncates, rejects, or accepts 200-char values.
    # Do not guess the next-screen title or an error string until that is observed.


def test_checkout_accepts_unicode_values(checkout_started: CheckoutPage):
    checkout_started.fill_information("ソリッド", "スネーク", "〒100-0001")
    # TODO: confirm whether unicode names/postcodes reach Overview or surface an error.
    # Do not guess the message or title until that is observed.
