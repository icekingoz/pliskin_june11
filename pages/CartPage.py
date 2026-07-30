from playwright.sync_api import Page

from pages.CheckoutPage import CheckoutPage


class CartPage:
    """The cart screen at /cart.html — everything you can see and do on that page."""

    def __init__(self, page: Page) -> None:
        # Locators
        self.page = page
        self.title = page.locator("[data-test=\"title\"]")

        # One locator can match MANY elements. cart_items matches every row in the cart.
        self.cart_items = page.locator("[data-test=\"inventory-item\"]")
        self.item_names = page.locator("[data-test=\"inventory-item-name\"]")
        self.item_prices = page.locator("[data-test=\"inventory-item-price\"]")
        self.item_quantities = page.locator("[data-test=\"item-quantity\"]")

        self.checkout_button = page.locator("[data-test=\"checkout\"]")
        self.continue_shopping_button = page.locator("[data-test=\"continue-shopping\"]")

        # Burger menu (used by logout)
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("[data-test=\"logout-sidebar-link\"]")

    # Methods (Wrapper)
    def start_checkout(self) -> CheckoutPage:
        # We navigate to a NEW screen, so we return that screen's page object.
        self.checkout_button.click()
        return CheckoutPage(self.page)

    def continue_shopping(self):
        # Navigates back to the inventory page.
        # The import is INSIDE the method to avoid a circular import
        # (InventoryPage imports CartPage at the top of its file).
        from pages.InventoryPage import InventoryPage

        self.continue_shopping_button.click()
        return InventoryPage(self.page)

    def remove_item(self, item_id: str):
        # item_id looks like "sauce-labs-backpack".
        # The remove button changes per product, so we build the locator here
        # instead of in __init__.
        self.page.locator(f"[data-test=\"remove-{item_id}\"]").click()
        # We stay on the SAME screen, so we return self. That lets us chain calls:
        # cart_page.remove_item("a").remove_item("b")
        return self

    def logout(self):
        # Same circular-import escape: LoginPage -> InventoryPage -> CartPage -> LoginPage
        # would be a loop if this import sat at the top of the file.
        # Importing here means it runs when the method is CALLED, not at import time.
        from pages.LoginPage import LoginPage

        self.menu_button.click()
        self.logout_link.click()
        return LoginPage(self.page)

    # Getters (are used for assertions later.)
    def get_title(self):
        return self.title

    def get_item_count(self):
        # How many rows are in the cart right now.
        return self.cart_items.count()

    def get_item_names(self):
        # Every product name in the cart, as a Python list of strings.
        return self.item_names.all_text_contents()

    def get_item_prices(self):
        # Turn "$29.99" into 29.99 so we can compare numbers
        prices = []
        for price_text in self.item_prices.all_text_contents():
            prices.append(float(price_text.replace("$", "")))
        return prices

    def get_checkout_button(self):
        return self.checkout_button

    def get_row_for(self, item_name: str):
        # filter(has_text=...) narrows the list of rows down to the one
        # containing that text. Reads the way a user thinks about the page.
        return self.cart_items.filter(has_text=item_name)

    # CLASSES SHOULD NOT HAVE ANY ASSERTS(or Expects)
