"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from catalog import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="home"),
    # CATALOG AND FILTERING
    path("catalog/", views.all_products, name="all_products"),
    # Use only the category slug (simpler and nicer URLs)
    path(
        "catalog/<slug:category_slug>/",
        views.all_products,
        name="product_list_by_category",
    ),
    # PRODUCT
    # Include slug in product URLs for SEO
    path(
        "product/<int:pk>/<slug:product_slug>/",
        views.product_detail,
        name="product_detail",
    ),
    # CART
    path("cart/", views.cart_detail, name="cart_detail"),
    path(
        "cart/add/<int:product_id>/", views.cart_add, name="cart_add"
    ),  # slug is optional here, but can be kept
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    # ORDERS
    path("order/create/", views.order_create, name="order_create"),
]

# This allows Django to serve uploaded media files during development:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
