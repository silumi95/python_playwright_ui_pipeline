import pytest
from playwright.sync_api import sync_playwright
from utils.test_utils import capture_screenshot
@pytest.mark.metadata(severity="Medium", priority="P2", executed_by="Silumi", defect="None")
def test_add_item_to_cart():
    """Test adding one item to cart"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.saucedemo.com/", timeout=40000)
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")

        try:
            page.click("button[data-test='add-to-cart-sauce-labs-backpack']")
            badge_text = page.inner_text(".shopping_cart_badge")
            assert badge_text == "1", "Item not added to cart."
        except Exception:
            capture_screenshot(page, "test_add_item_to_cart_failed")
            raise
        finally:
            browser.close()
