import pytest
from playwright.sync_api import sync_playwright
from utils.test_utils import capture_screenshot
@pytest.mark.metadata(severity="Medium", priority="P2", executed_by="Silumi", defect="None")
def test_logout_after_login():
    """Test logout functionality"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.saucedemo.com/", timeout=30000)
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")

        try:
            page.click("#react-burger-menu-btn")
            page.click("#logout_sidebar_link")
            assert "saucedemo.com" in page.url, "Logout failed."
        except Exception:
            capture_screenshot(page, "test_logout_after_login_failed")
            raise
        finally:
            browser.close()
