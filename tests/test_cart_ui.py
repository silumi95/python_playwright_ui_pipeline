import pytest
from playwright.sync_api import Page
@pytest.mark.metadata(severity="Medium", priority="P2", executed_by="Silumi", defect="None")
def test_valid_login(page: Page):
    """Test adding one item to cart"""

    page.goto("https://www.saucedemo.com/", timeout=40000)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    page.click("button[data-test='add-to-cart-sauce-labs-backpack']")
    badge_text = page.inner_text(".shopping_cart_badge")
    assert badge_text == "1", "Item not added to cart."
