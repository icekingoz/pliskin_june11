from playwright.sync_api import Page

def test_playwright_is_working(page: Page):
    page.goto("https://www.google.com")
    assert page.title() == "Google"