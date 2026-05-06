import re
from playwright.sync_api import Page, expect



def test_shop_page_accessible(page: Page, base_url: str):
    """Test that the shop page is accessible."""
    page.goto(base_url)
    page.locator("#navbarNav").get_by_role("link", name="Shop").click()
    expect(page).to_have_url(re.compile(".*/catalog/"))


def test_homepage_accessible(page: Page, base_url: str):
    """Test that the homepage is accessible."""
    page.goto(base_url)
    expect(page).to_have_title("KOROL LEATHER WORKSHOP")
    expect(page).to_have_url(base_url)


def test_category_page_accessible(page: Page, base_url: str):
    """Test that the category page is accessible."""
    page.goto(f"{base_url}catalog/wallets/")
    expect(page).to_have_url(re.compile(".*/wallets/"))
    expect(page.get_by_role("heading", name="Wallets")).to_be_visible()


def test_product_detail_page_accessible(page: Page, base_url: str):
    """Test that the product detail page is accessible."""
    page.goto(f"{base_url}catalog/")
    page.locator(".card a").first.click()
    product_header = page.locator("h1")
    expect(product_header).to_be_visible()


def test_cart_page_accessible(page: Page, base_url: str):
    """Test that the cart page is accessible."""
    page.goto(f"{base_url}cart/")
    expect(page).to_have_url(re.compile(".*/cart/"))
    expect(page.get_by_role("heading", name="Your Shopping Cart")).to_be_visible()
