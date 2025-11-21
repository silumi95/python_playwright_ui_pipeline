import pytest
from playwright.sync_api import Page
@pytest.mark.metadata(severity="Medium", priority="P2", executed_by="Silumi", defect="None")
def test_logout_after_login(page: Page):
  """Test logout functionality"""
  page.goto("https://www.saucedemo.com/", timeout=30000)
  page.fill("#user-name", "standard_user")
  page.fill("#password", "secret_sauce")
  page.click("#login-button")
  page.click("#react-burger-menu-btn")
  page.click("#logout_sidebar_link")
  assert "saucedemo.com" in page.url, "Logout failed."
       
