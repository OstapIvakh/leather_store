from django.test import TestCase, Client
from django.urls import reverse
from catalog.models import Product, Category

class LeatherStoreTests(TestCase):
    def setUp(self):
        """Налаштування даних перед кожним тестом"""
        self.client = Client()
        # Створюємо тестову категорію та товар
        self.category = Category.objects.create(name="Wallets", slug="wallets")
        self.product = Product.objects.create(
            name="Classic Wallet",
            slug="classic-wallet",
            price=50.00,
            category=self.category,
            is_available=True
        )

    def test_homepage_status_code(self):
        """Перевірка, чи відкривається головна сторінка магазину"""
        response = self.client.get(reverse('all_products'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        """Перевірка сторінки конкретного товару"""
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Classic Wallet")

    def test_cart_logic(self):
        """Перевірка додавання товару в кошик (сесії)"""
        # Імітуємо POST-запит на додавання в кошик
        # Переконайся, що назва 'cart_add' збігається з твоєю в urls.py
        response = self.client.post(reverse('cart_add', args=[self.product.id]), {'quantity': 1})
        
        # Перевіряємо редирект (зазвичай після додавання йде редирект на сторінку кошика)
        self.assertEqual(response.status_code, 302)
        
        # Перевіряємо, чи товар з'явився в сесії
        session = self.client.session
        self.assertIn(str(self.product.id), session.get('cart', {}))