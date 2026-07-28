import pytest
from playwright.sync_api import Page

from pages.LoginPage import LoginPage

# Level 1 check element exit, or are visible and work
def test_sort_dropdown_visible(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    inventory_page = login_page.login_standard_user()

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
def test_sort_options(page: Page, options):
    login_page = LoginPage(page)
    login_page.open()
    inventory_page = login_page.login_standard_user()

    inventory_page.sort_products_by(options)

    assert inventory_page.get_selected_sort() == options


def test_sort_dropdown_count(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    inventory_page = login_page.login_standard_user()

    assert inventory_page.get_sort_option_count() == 4


