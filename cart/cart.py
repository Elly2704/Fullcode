from decimal import Decimal
from shop.models import ProductProxy


class Cart():

    def __init__(self, request) -> None:
        self.session = request.session
        cart = self.session.get('session_key')
        if not cart:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = ProductProxy.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity, 'price': str(product.price)}

        self.cart[product_id]['quantity'] += quantity
        self.session.modified = True

    def delete(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product]
            self.session.modified = True

    def update(self, product, quantity):
        product_id = str(product)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
