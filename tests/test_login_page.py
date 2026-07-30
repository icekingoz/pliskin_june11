import pytest 

from playwright.sync_api import Page

from pages.LoginPage import LoginPage
from pages.InventoryPage import InventoryPage
 
 
def test_login_credentials(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    # assert (login_page.get_login_credentials.all_text_contents()).to_contain_text("standard_user")
    assert "standard_user" in login_page.get_login_credentials().inner_html()
    assert "secret_sauce" in login_page.get_login_password().inner_html()
 
def test_login_successful_one(page: Page):
    # Login Object only has to to Loging locators and Methods
    login_page = LoginPage(page)
    login_page.open()
    login_page.login_standard_user()
    # Only has access to Invetory stuff
    invetory_page = InventoryPage(page)
    assert invetory_page.get_title().text_content() == "Products"
   

@pytest.mark.parametrize(
    "username",
    [
        ("standard_user"),
        ("problem_user"),
        ("performance_glitch_user"),
        ("visual_user"),
    ],
)
def test_login_successful(page: Page, username):
    # Login Object only has to to Loging locators and Methods
    login_page = LoginPage(page)
    login_page.open()
    login_page.login_user(username, "secret_sauce")
    # Only has access to Invetory stuff
    invetory_page = InventoryPage(page)
    # page.wait_for_selector(invetory_page.get_title())
    assert invetory_page.get_title().text_content() == "Products"

# Negative as well
@pytest.mark.parametrize(
    "username, error",
    [
        ("locked_out_user", "Epic sadface: Sorry, this user has been locked out."),
        ("not_a_user", "Epic sadface: Username and password do not match any user in this service"),
    ],
)
def test_login_fails(page: Page, username, error):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login_user(username, "secret_sauce")

    actual_error = login_page.get_error_message().text_content()
    #    expected  vs  actual
    assert error in actual_error
