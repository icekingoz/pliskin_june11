import pytest

from pages.LoginPage import LoginPage


def test_login_credentials(login_page: LoginPage):
    assert "standard_user" in login_page.get_login_credentials().inner_html()
    assert "secret_sauce" in login_page.get_login_password().inner_html()


def test_login_successful_one(login_page: LoginPage):
    # login_standard_user() RETURNS the next page object. Use it.
    inventory_page = login_page.login_standard_user()
    assert inventory_page.get_title().text_content() == "Products"


@pytest.mark.parametrize(
    "username",
    [
        ("standard_user"),
        ("problem_user"),
        ("performance_glitch_user"),
        ("visual_user"),
    ],
)
def test_login_successful(login_page: LoginPage, username):
    inventory_page = login_page.login_user(username, "secret_sauce")
    assert inventory_page.get_title().text_content() == "Products"


LOCKED_OUT = "Epic sadface: Sorry, this user has been locked out."
BAD_CREDENTIALS = (
    "Epic sadface: Username and password do not match any user in this service"
)
USERNAME_REQUIRED = "Epic sadface: Username is required"
PASSWORD_REQUIRED = "Epic sadface: Password is required"


@pytest.mark.parametrize(
    "username, password, error",
    [
        ("locked_out_user", "secret_sauce", LOCKED_OUT),
        ("standard_user", "wrong_password", BAD_CREDENTIALS),
        ("not_a_user", "secret_sauce", BAD_CREDENTIALS),
        ("", "secret_sauce", USERNAME_REQUIRED),
        ("standard_user", "", PASSWORD_REQUIRED),
        ("", "", USERNAME_REQUIRED),
    ],
)
def test_login_fails(login_page: LoginPage, username, password, error):
    login_page.login_user(username, password)
    assert login_page.get_error_message().text_content() == error