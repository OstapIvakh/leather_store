from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Product, Category, OrderItem
from .forms import OrderCreateForm, ProductFilterForm
from .cart import Cart
from .utils import send_telegram_message
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q


def index(request):
    # Homepage: for now, show only the latest 3 products.
    latest_products = Product.objects.filter(is_available=True).order_by("-created_at")[
        :3
    ]
    return render(request, "catalog/index.html", {"latest_products": latest_products})


def all_products(request, category_slug=None):
    # Read raw query params from the URL.
    form = ProductFilterForm(request.GET)

    # Initialize variables upfront.
    min_price = None
    max_price = None

    # Django validates that values are numeric and non-negative.
    if form.is_valid():
        # Store cleaned values.
        min_price = form.cleaned_data.get("min_price")
        max_price = form.cleaned_data.get("max_price")

    category = None
    # Fetch all categories from the database.
    categories = Category.objects.all()
    # Fetch all available products from the database.
    products = Product.objects.filter(is_available=True)
    # If a category is provided, filter products by that category.

    # Get the search query from the search field.
    query = request.GET.get("search")
    if query:
        # Search in name OR description.
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # If no category is provided, keep the full product list.
    if category_slug:
        # Look up the category by slug.
        category = get_object_or_404(Category, slug=category_slug)
        # Filter products by the selected category.
        products = products.filter(category=category)

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Sorting.
    sort = request.GET.get("sort")

    if sort == "price_asc":
        products = products.order_by("price")  # Lowest price first
    elif sort == "price_desc":
        products = products.order_by("-price")  # Highest price first
    elif sort == "newest":
        products = products.order_by("-created_at")  # Newest first
    else:
        products = products.order_by("name")  # Default (alphabetical)

    # Create a paginator.
    # The second argument is items per page.
    paginator = Paginator(products, 3)

    # Current page number from the URL (e.g., ?page=2).
    page_number = request.GET.get("page")

    # Page object for the requested page.
    page_obj = paginator.get_page(page_number)

    # Render results.
    return render(
        request,
        "catalog/product_list.html",
        {
            "category": category,  # Used by the template for the page heading
            "categories": categories,  # Used to render the menu
            "products": page_obj,  # Pass a Page object instead of a full queryset
            "form": form,  # Filter form for the template
        },
    )


def product_detail(request, pk, product_slug):
    # Look up the product by ID and slug; raise 404 if not found.
    product = get_object_or_404(Product, id=pk, slug=product_slug, is_available=True)
    # Render the product detail template.
    return render(request, "catalog/product_detail.html", {"product": product})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # Quantity from the form; default to 1.
    quantity = int(request.POST.get("quantity", 1))

    # Check whether the request asks to override quantity (from the cart page).
    override = request.POST.get("override") == "True"

    cart.add(product=product, quantity=quantity, override_quantity=override)

    # Check if the user clicked "Buy Now".
    if request.POST.get("buy_now"):
        return redirect(
            "cart_detail"
        )  # For now redirect to cart; later this could go to checkout

    # For a regular "Add to Cart", return the user to the page they were on.
    return redirect(request.META.get("HTTP_REFERER", "all_products"))


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "catalog/cart_detail.html", {"cart": cart})


def order_create(request):
    cart = Cart(request)  # Initialize cart first

    # If the cart is empty, do not allow checkout.
    if len(cart) == 0:
        return redirect("all_products")

    if request.method == "POST":
        # 1. If the user submitted the form, populate it with POST data.
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # 2. Save the order header to the DB (create an Order instance).
            order = form.save()

            # Build a message body for internal notifications.
            items_text = ""
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
                items_text += f" - {item['product'].name} x {item['quantity']}\n"

            # Final Telegram message for the new order.
            tg_message = (
                f"<b>🚀 New Order #{order.id}</b>\n\n"
                f"<b>Customer:</b> {order.first_name} {order.last_name}\n"
                f"<b>Phone:</b> <code>{order.phone_number}</code>\n"
                f"<b>City:</b> {order.city}\n"
                f"<b>Postal code:</b> {order.postal_code}\n\n"
                f"<b>Items:</b>\n{items_text}\n"
                f"<b>Total:</b> {cart.get_total_price()}€"
            )

            send_telegram_message(tg_message)

            # 3. Send an email with order information.
            subject = f"Order #{order.id} Connfirmation"
            message = (
                f"Dear {order.first_name}!\n\n"
                f"Thank you for your order! Your order ID is {order.id}.\n\n"
                f"We will contact you soon to confirm the order details.\n\n"
                f"Best regards,\n"
                f"Korol Leather Workshop\n"
                f"https://korol-leather.com\n"
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [order.email],
                fail_silently=False,
            )

            # 4. Clear the cart after a successful order.
            cart.clear()

            # 5. Render the "Thank you for your order" page.
            return render(request, "catalog/order_created.html", {"order": order})
    else:
        # 6. If the user just opened the page, show an empty form.
        form = OrderCreateForm()

    return render(request, "catalog/order_create.html", {"cart": cart, "form": form})
