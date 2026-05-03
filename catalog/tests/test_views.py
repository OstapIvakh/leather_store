from django.test import TestCase, Client
from django.urls import reverse
from catalog.models import Product, Category


class LeatherStoreTests(TestCase):
    def setUp(self):
        """Set up data before each test."""
        self.client = Client()
        # Create a test category and product.
        self.category = Category.objects.create(name="Wallets", slug="wallets")
        self.product = Product.objects.create(
            name="Classic Wallet",
            slug="classic-wallet",
            price=50.00,
            category=self.category,
            is_available=True,
        )

    def test_homepage_status_code(self):
        """Verify that the shop homepage opens."""
        response = self.client.get(reverse("all_products"))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        """Verify a specific product detail page."""
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Classic Wallet")

    def test_cart_logic(self):
        """Verify adding a product to the cart (session)."""
        # Simulate a POST request to add the item to the cart.
        # Ensure that the 'cart_add' URL name matches the one in urls.py.
        response = self.client.post(
            reverse("cart_add", args=[self.product.id]), {"quantity": 1}
        )

        # Check redirect (typically after adding, it redirects to the cart page).
        self.assertEqual(response.status_code, 302)

        # Verify that the product appears in the session cart.
        session = self.client.session
        self.assertIn(str(self.product.id), session.get("cart", {}))
