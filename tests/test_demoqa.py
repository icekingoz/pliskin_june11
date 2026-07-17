import re
from playwright.sync_api import Page, expect
import pytest


@pytest.mark.parametrize(
    "first, last, email",
    [
        ("John", "Smith", "johnsmith@gmail.com"),
        ("Jane", "Doe", "janedoe@gmail.com"),
        ("Maria", "Garcia", "mariagarcia@yahoo.com"),
        ("Wei", "Chen", "weichen@outlook.com"),
        ("Aisha", "Patel", "aishapatel@proton.me"),
    ],
)
def test_form(page: Page, first, last, email) -> None:
    # Arrange
    page.goto("https://demoqa.com/automation-practice-form")
    # Act 
    page.get_by_role("textbox", name="First Name").fill(first)
    page.get_by_role("textbox", name="Last Name").fill(last)
    page.get_by_role("textbox", name="name@example.com").fill(email)
    page.get_by_role("radio", name="Male", exact=True).check()
    page.get_by_role("textbox", name="Mobile Number").fill("1231234567")
    page.get_by_role("button", name="Submit").click()
    # Assert
    expect(page.locator("#example-modal-sizes-title-lg")).to_contain_text("Thanks for submitting the form")
