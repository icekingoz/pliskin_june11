from playwright.sync_api import Page

# NEW: the inventory page can navigate to the cart, so it needs the cart's page object.
from pages.CartPage import CartPage


class InventoryPage:
    def __init__(self, page: Page) -> None:
        # Locators
        self.page = page
        self.title = page.locator("[data-test=\"title\"]")

        self.inventory_items = page.locator("[data-test=\"inventory-item\"]")
        self.item_names = page.locator("[data-test=\"inventory-item-name\"]")
        self.item_descriptions = page.locator("[data-test=\"inventory-item-desc\"]")
        self.item_prices = page.locator("[data-test=\"inventory-item-price\"]")

        self.sort_dropdown = page.locator("[data-test=\"product-sort-container\"]")
        self.sort_options = self.sort_dropdown.locator("option")

        # NEW: the cart icon in the top-right corner
        self.cart_link = page.locator("[data-test=\"shopping-cart-link\"]")

    # Methods (Wrapper)
    def add_item_to_cart(self, item_id: str):
        self.page.locator(f"[data-test=\"add-to-cart-{item_id}\"]").click()
        return self

    def sort_products_by(self, option: str):
        # option is one of: az, za, lohi, hilo
        self.sort_dropdown.select_option(option)

    # NEW: clicking the cart icon takes us to a different screen,
    # so this method returns the CartPage object for that screen.
    def open_cart(self) -> CartPage:
        self.cart_link.click()
        return CartPage(self.page)

    # Getters (are used for assertions later.)
    def get_title(self):
        return self.title

    def get_sort_dropdown(self):
        return self.sort_dropdown

    def get_product_count(self):
        return self.inventory_items.count()

    def get_sort_option_count(self):
        return self.sort_options.count()

    def get_selected_sort(self):
        # Returns the value of the selected option, for example "az"
        return self.sort_dropdown.input_value()

    def get_item_names(self):
        return self.item_names.all_text_contents()

    def get_item_descriptions(self):
        return self.item_descriptions.all_text_contents()

    def get_item_prices(self):
        # Turn "$29.99" into 29.99 so we can compare numbers
        prices = []
        for price_text in self.item_prices.all_text_contents():
            prices.append(float(price_text.replace("$", "")))
        return prices

    # CLASSES SHOULD NOT HAVE ANY ASSERTS(or Expects)
