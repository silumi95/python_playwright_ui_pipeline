import pytest
from playwright.sync_api import Page
@pytest.mark.metadata(severity="Medium", priority="P2", executed_by="Silumi", defect="LoginError")
def test_invalid_credentials(page):
    """Login attempt with invalid credentials"""
    
    page.goto("https://www.saucedemo.com/", timeout=30000)
    page.fill("#user-name", "invalid_user")
    page.fill("#password", "wrong_password")
    page.click("#login-button")
    error_text = page.inner_text("h3[data-test='error']")
    assert "do not match" in error_text, "Expected error not displayed."
      


@pytest.mark.metadata(severity="Low", priority="P3", executed_by="Silumi", defect="None")
def test_empty_fields(page: Page):
    """Attempt login with empty username and password"""

    page.goto("https://www.saucedemo.com/", timeout=30000)
    page.click("#login-button")
    error_text = page.inner_text("h3[data-test='error']")
    assert "Username is required" in error_text, "Expected empty field error not shown."
        


@pytest.mark.metadata(severity="High", priority="P1", executed_by="Silumi", defect="LockedUser")
def test_locked_out_user(page: Page):
    """Locked-out user should not be able to log in"""

    page.goto("https://www.saucedemo.com/", timeout=30000)
   
    page.fill("#user-name", "locked_out_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    error_text = page.inner_text("h3[data-test='error']")
    assert "locked out" in error_text.lower(), "Locked-out message not displayed."

