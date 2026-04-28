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
    # Головна сторінка, поки показуємо тільки останні 3 товари
    latest_products = Product.objects.filter(is_available=True).order_by('-created_at')[:3]
    return render(request, 'catalog/index.html', {'latest_products': latest_products})

def all_products(request, category_slug=None):
    # беремо "брудні" дані з URL.
    form = ProductFilterForm(request.GET)

    # Ініціалізуємо змінні заздалегідь
    min_price = None
    max_price = None

    # Django перевіряє, чи там цифри, і чи вони не від'ємні.
    if form.is_valid():
        # Записуємо чисті данні у змінні
        min_price = form.cleaned_data.get('min_price') 
        max_price = form.cleaned_data.get('max_price')

    category = None
    #Вибираємо всі категорії з бази даних
    categories = Category.objects.all()
    #Вибираємо всі товари з бази даних
    products = Product.objects.filter(is_available=True)
    #Якщо є категорія, то вибираємо тільки ті товари, які належать до цієї категорії
    
    # Отримуємо запит із пошукового рядка (назвемо параметр 'query')
    query = request.GET.get('search')
    if query:
        # Шукаємо одночасно в назві АБО в описі
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    #Якщо немає категорії, то вибираємо всі товари
    if category_slug:
        #Вибираємо категорію за її slug
        category = get_object_or_404(Category, slug=category_slug)
        #Вибираємо тільки ті товари, які належать до цієї категорії
        products = products.filter(category=category)

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Отримуємо параметр сортування
    sort = request.GET.get('sort')

    if sort == 'price_asc':
        products = products.order_by('price') # Від дешевих
    elif sort == 'price_desc':
        products = products.order_by('-price') # Від дорогих
    elif sort == 'newest':
        products = products.order_by('-created_at') # Новинки
    else:
        products = products.order_by('name') # За замовчуванням (алфавіт)
        

    # Створюємо об'єкт пагінатора. 
    # Другий аргумент — це кількість товарів на сторінці (давай поставимо 6 для тесту).
    paginator = Paginator(products, 3)

    # Отримуємо номер поточної сторінки з URL (наприклад, ?page=2)
    page_number = request.GET.get('page')

    # Отримуємо об'єкт сторінки з товарами саме для цього номера
    page_obj = paginator.get_page(page_number)
        

    #Відправляємо результат у шаблон
    return render(request, 'catalog/product_list.html', {
        'category': category, #Передаємо категорію, щоб написати заголовок
        'categories': categories, #Передаємо всі категорії, щоб показати в меню
        'products': page_obj, #Tепер у шаблон замість 'products' передаємо 'page_obj 
        'form': form,  # Передаємо форму фільтрації для використання у шаблоні
        })

def product_detail(request, pk, product_slug):
    # Шукаємо товар за його ID та slug. Якщо не знайдемо — покажемо помилку 404
    product = get_object_or_404(Product, id=pk, slug=product_slug, is_available=True)
    # Відправляємо товар у "шаблон" (HTML-файл) 
    return render(request, 'catalog/product_detail.html', {'product': product})
    

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # Отримуємо кількість з форми, якщо її немає — за замовчуванням 1   
    quantity = int(request.POST.get('quantity', 1))

    # Перевіряємо, чи прийшов запит на перезапис (з кошика)
    override = request.POST.get('override') == 'True'

    cart.add(product=product, quantity=quantity, override_quantity=override)

    # Перевіряємо, чи була натиснута кнопка "Buy Now"
    if request.POST.get('buy_now'):
        return redirect('cart_detail') # Поки шлемо в кошик, пізніше — на оплату
    
    # Якщо просто "Add to Cart", повертаємо на ту ж сторінку, де був юзер
    return redirect(request.META.get('HTTP_REFERER', 'all_products'))

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'catalog/cart_detail.html', {'cart': cart})

def order_create(request):
    cart = Cart(request) # Спочатку ініціалізуємо кошик

    # Якщо кошик порожній, не пускаємо на сторінку оформлення
    if len(cart) == 0:
        return redirect('all_products')

    if request.method == 'POST':
        # 1. Якщо юзер натиснув "Оформити", наповнюємо форму даними з запиту
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # 2. Зберігаємо "шапку" замовлення в базу (створюємо об'єкт Order)
            order = form.save()

            # Формуємо текст повідомлення для себе 
            items_text = ""
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                items_text += f" - {item['product'].name} x {item['quantity']}\n"

            # Фінальний текст повідомлення про нове замовлення в Telegram
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

            # 3 Відправляємо електронну пошту з інформацією про замовлення
            subject = f'Order #{order.id} Connfirmation'
            message = (
                f'Dear {order.first_name}!\n\n'
                f'Thank you for your order! Your order ID is {order.id}.\n\n'
                f'We will contact you soon to confirm the order details.\n\n'
                f'Best regards,\n'
                f'Korol Leather Workshop\n'
                f'https://korol-leather.com\n'
                )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [order.email],
                fail_silently=False,
            )
            
            
            # 4. Очищаємо кошик після успішного замовлення
            cart.clear()
            
            # 5. Показуємо сторінку "Дякуємо за замовлення!"
            return render(request, 'catalog/order_created.html', {'order': order})
    else:
        # 6. Якщо юзер просто зайшов на сторінку — показуємо йому порожню форму
        form = OrderCreateForm()
    
    return render(request, 'catalog/order_create.html', {'cart': cart, 'form': form})