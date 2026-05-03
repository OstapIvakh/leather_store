from django.contrib import admin
from .models import Product, Category, ProductImage, Order, OrderItem


# Allows adding photos directly on the product admin page.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # How many empty image rows to show by default


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}  # Auto-fill slug from name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "is_available", "category"]
    list_filter = ["is_available", "category"]
    search_fields = ["name"]
    list_editable = ["price", "is_available", "category"]
    list_per_page = 10
    inlines = [ProductImageInline]  # Add image gallery to the product admin
    prepopulated_fields = {"slug": ("name",)}  # Auto-fill slug from name


# 1. Inline items for orders.
# This allows editing order items directly on the order admin page.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]  # Easier product lookup by ID


# 2. Configure the Order admin view.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Columns shown in the list view.
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "country",
        "city",
        "address",
        "postal_code",
        "phone_number",
        "paid",
        "date",
        "get_total_cost",
    ]

    # Right-side filters (paid status, date, etc.).
    list_filter = ["paid", "date", "country"]

    # Allow editing the "paid" field directly in the list view.
    list_editable = ["paid"]

    # Show order items inline.
    inlines = [OrderItemInline]
