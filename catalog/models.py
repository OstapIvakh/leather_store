from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200)
    # Slug — це те саме "людське посилання" (наприклад, 'wallets')
    slug = models.SlugField(max_length=200, db_index=True, blank=True)

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.id, self.slug])

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    # Додаємо зв'язок: один товар належить до однієї категорії
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    slug = models.SlugField(max_length=200, db_index=True, blank=True)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])
    # def get_absolute_url(self):
    # return reverse('catalog:product_detail', args=[self.id, self.slug])
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"

class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Czech Republic')
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date'] # Нові замовлення будуть зверху

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.price * item.quantity for item in self.items.all())

    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
