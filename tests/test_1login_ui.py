import pytest
from playwright.sync_api import sync_playwright
from utils.test_utils import capture_screenshot

@pytest.mark.metadata(severity="High", priority="P1", executed_by="Silumi", defect="None")
def test_valid_login():
    """Test valid login with standard_user"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.saucedemo.com/", timeout=30000)

        try:
            page.fill("#user-name", "standard_user")
            page.fill("#password", "secret_sauce")
            page.click("#login-button")
            assert "inventory" in page.url, "Login failed."
        except Exception:
            capture_screenshot(page, "test_valid_login_failed")
            raise
        finally:
            browser.close()
