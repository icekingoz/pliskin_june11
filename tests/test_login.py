import re
from playwright.sync_api import Page, expect


def test_example_1(page: Page) -> None:
    page.goto("")
    #      LOCATE               .             ACTIONS
    page.locator("[data-test=\"username\"]").click() # click on the username field
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"password\"]").click()
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"secondary-header\"]")).to_be_visible()

    # expect == assert
    # 1. Go to Page
    # 2. Locate the element
    # 3. Action on the element
    # Expected Result = Actual Result

def test_example_2(page: Page) -> None:
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test=\"username\"]").click()
    page.locator("[data-test=\"username\"]").fill("locked_out_user")
    page.locator("[data-test=\"password\"]").click()
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_contain_text("Epic sadface: Sorry, this user has been locked out.")
