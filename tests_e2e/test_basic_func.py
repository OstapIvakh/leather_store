import re
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8000/"


def test_homepage_accessible(page: Page):
    page.goto(BASE_URL)
    expect(page).to_have_title("KOROL LEATHER WORKSHOP")
    expect(page).to_have_url(BASE_URL)


def test_category_page_accessible(page: Page):
    page.goto(f"{BASE_URL}/catalog/wallets/")
    expect(page).to_have_url(re.compile(".*/wallets/"))
    header = page.get_by_role("heading", name="Wallets")
    expect(header).to_be_visible()


def test_product_detail_page_accessible(page: Page):
    page.goto(f"{BASE_URL}/product/1/classic-bifold-wallet/")
    product_header = page.get_by_role("heading", name="Classic bifold wallet")
    expect(product_header).to_be_visible()


def test_cart_page_accessible(page: Page):
    page.goto(f"{BASE_URL}/cart/")
    expect(page).to_have_url(re.compile(".*/cart/"))
    header = page.locator("h2")
    expect(header).to_have_text("Your Shopping Cart")
