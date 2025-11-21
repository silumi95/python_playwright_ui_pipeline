import pytest


@pytest.mark.metadata(severity="High", priority="P1", executed_by="Silumi", defect="None")
def test_valid_login(page):
    """Test valid login with standard_user"""
    page.goto("https://www.saucedemo.com/", timeout=30000)
    
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    assert "inventory" in page.url, "Login failed."
    # test