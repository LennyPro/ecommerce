from django.conf import settings
from decimal import Decimal
from inventory.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

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

    def __len__(self):
        return sum([item['quantity'] for item in self.cart.values()])

    # ======================== SAVE ===========================================
    def save(self):
        """Save changes to the session"""
        # self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    # =======================================================================
    # used by "update" <button> of cart_details.html
    def add(self, product, quantity=1, override=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    # removes a specific product from the cart
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # empties the entire cart, removing all products
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


'''In summary, this class handles all the necessary operations to manage the shopping cart's contents 
and interact with the session to maintain its state across user requests.'''

'''The Cart class in this Django application manages the shopping cart using session data. 
It initializes the cart from the session, allowing products to be added, removed, and iterated over. 

The __iter__ method retrieves product details from the database and calculates total prices. 
The cart’s state is saved whenever changes are made, and the total price of the cart can be calculated. 
It also supports clearing the cart and determining the total quantity of items. 
This ensures efficient cart management within the user's session.'''

