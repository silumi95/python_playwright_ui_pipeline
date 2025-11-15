import pytest
from playwright.sync_api import sync_playwright
from utils.test_utils import capture_screenshot
@pytest.mark.metadata(severity="Medium", priority="P2", executed_by="Silumi", defect="LoginError")
def test_invalid_credentials():
    """Login attempt with invalid credentials"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.saucedemo.com/", timeout=30000)
        try:
            page.fill("#user-name", "invalid_user")
            page.fill("#password", "wrong_password")
            page.click("#login-button")
            error_text = page.inner_text("h3[data-test='error']")
            assert "do not match" in error_text, "Expected error not displayed."
        except Exception:
            capture_screenshot(page, "test_invalid_credentials_failed")
            raise
        finally:
            browser.close()


@pytest.mark.metadata(severity="Low", priority="P3", executed_by="Silumi", defect="None")
def test_empty_fields():
    """Attempt login with empty username and password"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.saucedemo.com/")
        try:
            page.click("#login-button")
            error_text = page.inner_text("h3[data-test='error']")
            assert "Username is required" in error_text, "Expected empty field error not shown."
        except Exception:
            capture_screenshot(page, "test_empty_fields_failed")
            raise
        finally:
            browser.close()


@pytest.mark.metadata(severity="High", priority="P1", executed_by="Silumi", defect="LockedUser")
def test_locked_out_user():
    """Locked-out user should not be able to log in"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.saucedemo.com/")
        try:
            page.fill("#user-name", "locked_out_user")
            page.fill("#password", "secret_sauce")
            page.click("#login-button")
            error_text = page.inner_text("h3[data-test='error']")
            assert "locked out" in error_text.lower(), "Locked-out message not displayed."
        except Exception:
            capture_screenshot(page, "test_locked_out_user_failed")
            raise
        finally:
            browser.close()
