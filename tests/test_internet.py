# Test Case 1: Click Action
import uuid

from playwright.sync_api import Dialog, Page, expect
import pytest


def test_click_action(page: Page):
    add_element_button = page.get_by_role("button", name="Add Element")
    delete_button = page.get_by_role("button", name="Delete")
    # 1. Go to Page
    page.goto("https://the-internet.herokuapp.com/add_remove_elements/")
    # 2. Click on the Add Element button
    add_element_button.click()
    add_element_button.click()
    # 3. Click on the Delete button
    delete_button.first.click()
    # for b in delete_button.all():
    #     b.click()
    # Both are asserts, but one comes from playwright, the other from Pytest
    expect(delete_button).to_be_visible()
    assert delete_button.is_visible()



@pytest.mark.parametrize(
    "username, password, expected_text",
    [
        ("tomsmith", "SuperSecretPassword!", "Welcome to the Secure Area. When you are done click logout below."),
        ("invaliduser", "SuperSecretPassword!", "Your username is invalid!"),
        ("tomsmith", "wrongpassword", "Your password is invalid!"),
        ("johndoe", "password123", "Your username is invalid!"),
        ("tomsmith", "SuperSecretPassword", "Your password is invalid!"),
    ],
)
def test_fill_and_press(page: Page, username: str, password: str, expected_text: str) -> None:
    # 1. Go to Page
    page.goto("https://the-internet.herokuapp.com/login")
    username_field = page.get_by_label("Username")
    password_field = page.get_by_label("Password")

    username_field.fill(username)
    username_field.press("Tab")
    password_field.fill(password)
    password_field.press("Enter")

    # Store the text from the page as actual result THEN compare against expected result in assert statement
    if expected_text.startswith("Welcome"):
        actual_text = page.get_by_role("heading", name="Welcome to the Secure Area.").text_content()
    else:
        actual_text = page.locator("#flash").text_content()
    assert expected_text in actual_text




def test_checkboxes(page: Page):
    page.goto("https://the-internet.herokuapp.com/checkboxes")
    boxes = page.get_by_role("checkbox")

    boxes.first.check()
    boxes.last.uncheck()

    assert boxes.first.is_checked()
    assert not boxes.last.is_checked()


def test_dropdown(page: Page):
    page.goto("https://the-internet.herokuapp.com/dropdown")
    dropdown = page.locator("#dropdown")

    dropdown.select_option("2")
    dropdown.select_option(label="Option 1")
    dropdown.select_option(index=2)

def test_hovers(page: Page):
    page.goto("https://the-internet.herokuapp.com/hovers")
    image= page.locator(".figure").first
    image.hover()

def test_upload(page: Page):
    page.goto("https://the-internet.herokuapp.com/upload")
    #  locator of the input          path to the file
    page.locator("#file-upload").set_input_files("test_data/resume.txt")
    page.locator("#file-submit").click()

def test_drag_and_drop(page: Page):
    page.goto("https://the-internet.herokuapp.com/drag_and_drop")
    a = page.locator("#column-a")
    b = page.locator("#column-b")

    a.drag_to(b)
    b.drag_to(a)

def test_context_menu(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/context_menu")
    page.on("dialog", lambda dialog: dialog.accept())
    page.locator("#hot-spot").click(button="right")


def test_upload_then_download_roundtrip(page: Page, tmp_path) -> None:
    """/download lists whatever strangers upload, so hardcoded filenames rot.
    Fix: OWN the data — upload a uniquely named file, then download that exact file.
    (tmp_path is a pytest built-in fixture: a fresh temp folder per test.)"""
    file_name = f"pliskin-{uuid.uuid4().hex[:8]}.txt"
    local_file = tmp_path / file_name
    local_file.write_text("uploaded by the pliskin_june11 test suite")

    # Arrange: put our own file on the server
    page.goto("https://the-internet.herokuapp.com/upload")
    page.locator("#file-upload").set_input_files(local_file)
    page.locator("#file-submit").click()
    expect(page.locator("#uploaded-files")).to_have_text(file_name)

    # Act + assert: it must now appear on /download, under the name WE chose
    page.goto("https://the-internet.herokuapp.com/download")
    with page.expect_download() as download_info:
        page.get_by_role("link", name=file_name, exact=True).click()
    assert download_info.value.suggested_filename == file_name


def test_hidden_ad(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/entry_ad")
    modal = page.locator("#modal")
    # Wait for the modal to load
    modal.wait_for(state="visible")
    assert modal.is_visible()

    page.get_by_text("Close", exact=True).click()
    modal.wait_for(state="hidden")
    assert not modal.is_visible()