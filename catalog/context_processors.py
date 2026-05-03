from .models import Category
from .cart import Cart


def categories_processor(request):
    # Fetch all categories from the database.
    all_categories = Category.objects.all()
    # Return a dict that will be available in every template context.
    return {"all_categories": all_categories}


def cart(request):
    return {"cart": Cart(request)}
