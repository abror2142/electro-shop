from django.contrib.auth.models import User
from shop.models import Order, Product, OrderProduct, Wishlist
from django.http import HttpRequest
from accounts.models import Customer


class CartAuthenticatedUser:
    def __init__(self, request: HttpRequest, product_id=None, action=None):
        self.request = request

        if product_id and action:
            self.add_or_delete(product_id, action)

    def get_cart_info(self):
        customer, created = Customer.objects.get_or_create(
            user=self.request.user
        )

        order, created = Order.objects.get_or_create(
            customer=customer,
            active=True
        )
        return {
            'order': order,
            'order_products': OrderProduct.objects.filter(order=order),
            'total_cart_price': order.get_cart_total_price,
            'total_cart_product': order.get_total_cart_product,
            'total_product_number': order.get_cart_product_number
        }

    def add_or_delete(self, product_id, action):
        product = Product.objects.get(pk=product_id)
        order = self.get_cart_info()['order']
        order_product, created = OrderProduct.objects.get_or_create(
            order=order,
            product=product
        )

        if action == 'add' and order_product.product.quantity > order_product.quantity:
            order_product.quantity += 1
        elif action == 'remove':
            order_product.quantity -= 1

        order_product.save()

        if order_product.quantity <= 0 or action == 'delete':
            order_product.delete()


class UserWishlistManager:
    def __init__(self, request: HttpRequest, slug=None, action=None):
        self.request = request

        if slug and action:
            self.add_or_delete(slug, action)

    def get_wishlist_info(self):
        customer, created = Customer.objects.get_or_create(
            user=self.request.user
        )

        wishlist = Wishlist.objects.filter(
            customer=customer,
        )

        return {
            'wishlist_products': wishlist
        }

    def add_or_delete(self, slug, action):
        product = Product.objects.get(slug=slug)
        customer = Customer.objects.get(user=self.request.user)

        if action == 'add':
            Wishlist.objects.get_or_create(product=product, customer=customer)
        elif action == 'remove':
            wishlist = Wishlist.objects.get(product=product, customer=customer)
            wishlist.delete()
        elif action == 'clear':
            wishlist = Wishlist.objects.filter(customer=customer)
            wishlist.delete()
