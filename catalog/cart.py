from decimal import Decimal
from django.conf import settings
from .models import Product

class Cart:
    # Спрацьовує щоразу, коли ми звертаємося до кошика. 
    # Вона перевіряє: "У цього юзера вже є кошик у сесії? Якщо ні — створюю порожній словник {}"
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        # Це найважливіша частина для шаблону. Вона дозволяє нам написати в HTML {% for item in cart %}. 
        # Вона бере ID товарів з пам'яті, іде в базу даних, дістає об'єкти Product (з фото та назвами) і 
        # "склеює" їх з кількістю та ціною.
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # ця функ каже Django: "Агов, дані в сесії змінилися, збережи їх у базу сесій!". 
        # Без цього товари будуть зникати при переході на іншу сторінку.
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __len__(self):
        # Рахуємо загальну кількість товарів у кошику.
        return sum(item['quantity'] for item in self.cart.values())