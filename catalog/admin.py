from django.contrib import admin
from .models import Product, Category, ProductImage, Order, OrderItem

# Це дозволить додавати фото прямо в картці товару
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3 # Скільки порожніх полів для фото показувати за замовчуванням

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} # Автоматично заповнюємо поле slug на основі поля name

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_available', 'category']
    list_filter = ['is_available', 'category']
    search_fields = ['name']
    list_editable = ['price', 'is_available', 'category']
    list_per_page = 10
    inlines = [ProductImageInline] # Додаємо галерею в адмінку товару
    prepopulated_fields = {'slug': ('name',)} # Автоматично заповнюємо поле slug на основі поля name

# 1. Створюємо "вкладку" для товарів
# Це дозволить редагувати товари замовлення прямо на сторінці самого замовлення
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product'] # Зручний пошук товару за ID

# 2. Налаштовуємо відображення самого Замовлення
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Які колонки ми бачимо у загальному списку
    list_display = ['id', 'first_name', 'last_name', 'email', 'country', 
                    'city', 'address', 'postal_code', 'phone_number', 'paid', 'date', 
                     'get_total_cost']
    
    # Фільтри справа (зручно шукати тільки оплачені або за датою)
    list_filter = ['paid', 'date', 'country']

    # Можна редагувати поле "оплачено" прямо в списку
    list_editable = ['paid']
    
    # Додаємо товари всередину замовлення
    inlines = [OrderItemInline]

