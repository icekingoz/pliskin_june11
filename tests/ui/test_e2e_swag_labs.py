import pytest
from playwright.sync_api import Page, expect


@pytest.mark.parametrize(
    "product",
    [
        "sauce-labs-backpack",
        "sauce-labs-bike-light",
        "sauce-labs-bolt-t-shirt",
        "sauce-labs-fleece-jacket",
        "sauce-labs-onesie",
    ],
)
def test_checkout_happy_path(page: Page, product: str):
    # --- Log in ---
    page.goto("/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()
    # --- Add an item, open cart, check out ---
    page.locator(f"#add-to-cart-{product}").click()
    page.locator(".shopping_cart_link").click()
    page.locator("#checkout").click()
    page.locator("#first-name").fill("Solid")
    page.locator("#last-name").fill("Snake")
    page.locator("#postal-code").fill("00001")
    page.locator("#continue").click()
    page.locator("#finish").click()
    assert page.locator(".complete-header").inner_text()  == "Thank you for your order!"
    # expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")
