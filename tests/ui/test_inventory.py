import pytest
from playwright.sync_api import Page

from pages.InventoryPage import InventoryPage
from pages.LoginPage import LoginPage

INVENTORY_REQUIRES_LOGIN = (
    "Epic sadface: You can only access '/inventory.html' when you are logged in."
)


def _assert_inventory_not_visible(inventory_page: InventoryPage) -> None:
    assert not inventory_page.get_inventory_container().is_visible()
    assert not inventory_page.get_sort_dropdown().is_visible()
    assert not inventory_page.get_title().is_visible()
    assert "/inventory.html" not in inventory_page.page.url


def test_inventory_inaccessible_without_login_direct_url(page: Page):
    inventory_page = InventoryPage(page).open()

    _assert_inventory_not_visible(inventory_page)


def test_inventory_inaccessible_without_login_redirects_to_login(login_page: LoginPage):
    InventoryPage(login_page.page).open()

    assert login_page.login_button.is_visible()
    assert login_page.get_error_message().text_content() == INVENTORY_REQUIRES_LOGIN
    _assert_inventory_not_visible(InventoryPage(login_page.page))


def test_inventory_inaccessible_after_wrong_login_redirect(login_page: LoginPage):
    inventory_page = login_page.login_user("standard_user", "wrong_password")

    assert login_page.login_button.is_visible()
    _assert_inventory_not_visible(inventory_page)


def test_inventory_inaccessible_after_wrong_login_direct_url(login_page: LoginPage):
    login_page.login_user("standard_user", "wrong_password")
    inventory_page = InventoryPage(login_page.page).open()

    assert login_page.login_button.is_visible()
    assert login_page.get_error_message().text_content() == INVENTORY_REQUIRES_LOGIN
    _assert_inventory_not_visible(inventory_page)



# Level 1 check element exit, or are visible and work
def test_sort_dropdown_visible(inventory_page: InventoryPage):
    assert inventory_page.get_sort_dropdown().is_visible()


# Test actual functionality
@pytest.mark.parametrize(
    "options",
    [
        ("az"),
        ("za"),
        ("lohi"),
        ("hilo"),
    ],
)
def test_sort_options(inventory_page: InventoryPage, options):
    inventory_page.sort_products_by(options)

    assert inventory_page.get_selected_sort() == options


def test_sort_dropdown_count(inventory_page: InventoryPage):
    assert inventory_page.get_sort_option_count() == 4