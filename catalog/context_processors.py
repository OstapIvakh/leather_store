from .models import Category
from .cart import Cart

def categories_processor(request):
    # Дістаємо ВСІ категорії з бази
    all_categories = Category.objects.all()
    # Повертаємо словник, який буде доступний у будь-якому HTML-файлі
    return {'all_categories': all_categories}

def cart(request):
    return {'cart': Cart(request)}
