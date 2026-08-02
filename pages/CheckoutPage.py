from playwright.sync_api import Page


class CheckoutPage:
    """The whole checkout flow: information -> overview -> complete.

    Three URLs, but one meaningful journey for the user, so we keep it in one class.
    """

    def __init__(self, page: Page) -> None:
        # Locators
        self.page = page
        self.title = page.locator("[data-test=\"title\"]")

        # Step one — Your Information
        self.first_name = page.locator("[data-test=\"firstName\"]")
        self.last_name = page.locator("[data-test=\"lastName\"]")
        self.postal_code = page.locator("[data-test=\"postalCode\"]")
        self.continue_button = page.locator("[data-test=\"continue\"]")
        self.cancel_button = page.locator("[data-test=\"cancel\"]")
        self.error_message = page.locator("[data-test=\"error\"]")

        # Step two — Overview
        self.item_names = page.locator("[data-test=\"inventory-item-name\"]")
        self.item_prices = page.locator("[data-test=\"inventory-item-price\"]")
        self.subtotal_label = page.locator("[data-test=\"subtotal-label\"]")
        self.tax_label = page.locator("[data-test=\"tax-label\"]")
        self.total_label = page.locator("[data-test=\"total-label\"]")
        self.finish_button = page.locator("[data-test=\"finish\"]")

        # Step three — Complete
        self.complete_header = page.locator("[data-test=\"complete-header\"]")
        self.complete_text = page.locator("[data-test=\"complete-text\"]")
        self.back_home_button = page.locator("[data-test=\"back-to-products\"]")

    # Methods (Wrapper)
    def fill_information(self, first_name: str, last_name: str, postal_code: str):
        # Fills the form and clicks Continue.
        # NOTE: no assert in here. If the form is invalid we stay on step one and
        # the test can check the error itself. One method serves happy AND sad path.
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)
        self.continue_button.click()
        # Still inside the same checkout flow, so return self and keep chaining.
        return self

    def finish(self):
        # Confirms the order and lands on the "complete" screen.
        self.finish_button.click()
        return self

    def cancel(self):
        # Cancel takes us back out of checkout.
        from pages.InventoryPage import InventoryPage

        self.cancel_button.click()
        return InventoryPage(self.page)

    def back_home(self):
        # Only available on the final "Thank you" screen.
        # Local import again: it breaks the import loop between the page files.
        from pages.InventoryPage import InventoryPage

        self.back_home_button.click()
        return InventoryPage(self.page)

    # Getters (are used for assertions later.)
    def get_title(self):
        return self.title

    def get_error_message(self):
        return self.error_message

    def get_complete_header(self):
        return self.complete_header

    def get_complete_text(self):
        return self.complete_text

    def get_item_names(self):
        return self.item_names.all_text_contents()

    def get_item_count(self):
        return self.item_names.count()

    def get_total_label(self):
        return self.total_label

    def get_total(self):
        # "Total: $32.39" -> 32.39
        total_text = self.total_label.text_content()
        return float(total_text.split("$")[1])

    def get_subtotal(self):
        # "Item total: $29.99" -> 29.99
        subtotal_text = self.subtotal_label.text_content()
        return float(subtotal_text.split("$")[1])

    # CLASSES SHOULD NOT HAVE ANY ASSERTS(or Expects)
