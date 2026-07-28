from playwright.sync_api import Page

from pages.InventoryPage import InventoryPage


class LoginPage:
    # __int
    def __init__(self, page: Page) -> None:
        # Locators
        self.page = page
        self.username = page.locator("[data-test=\"username\"]")
        self.password = page.locator("[data-test=\"password\"]")
        self.login_button = page.locator("[data-test=\"login-button\"]")

        self.login_credentials = page.locator("[data-test=\"login-credentials\"]")
        self.login_password = page.locator("[data-test=\"login-password\"]")
        self.error_message = page.locator("[data-test=\"error\"]")
        self.error_close_button = page.locator("[data-test=\"error-button\"]")


    #Methods (Wrapper)
    def open(self):
        self.page.goto("/")

    def login_standard_user(self) -> InventoryPage:
        self.username.fill("standard_user")
        self.password.fill("secret_sauce")
        self.login_button.click()
        return InventoryPage(self.page)

    def login_user(self, username: str, password: str) -> InventoryPage:
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
        return InventoryPage(self.page)

    # def login_standard_user(self):
    #     self.login_user(self, "standard_user","secret_sauce")

    # Getters (are used for assertions later.)
    def get_login_credentials(self):
        return self.login_credentials

    def get_login_password(self):
        return self.login_password

    def get_error_message(self):
        return self.error_message

    # CLASSES SHOULD HAVE ANY ASSERTS(or Expects)

    