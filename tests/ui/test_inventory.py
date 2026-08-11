import pytest

from pages.InventoryPage import InventoryPage


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