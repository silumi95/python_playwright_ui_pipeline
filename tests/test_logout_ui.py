import pytest

@pytest.mark.metadata(
    severity="Medium", 
    priority="P2", 
    executed_by="Silumi", 
    defect="None",
    description="Validate user can logout successfully"
    )
def test_logout_after_login(page):
  """Test logout functionality"""
  page.goto("https://www.saucedemo.com/", timeout=30000)
  page.fill("#user-name", "standard_user")
  page.fill("#password", "secret_sauce")
  page.click("#login-button")
  page.click("#react-burger-menu-btn")
  page.click("#logout_sidebar_link")
  assert "saucedemo.com" in page.url, "Logout failed."
       
