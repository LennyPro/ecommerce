from django.db import models
from inventory.models import Product

ORDER_STATUS_CHOICES = (('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled'))


# Checkout
class Order(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=16)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, default='pending', max_length=10, blank=True, null=True)
    payment_id = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return f' order #{self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())  # self.items come from class OrderItem's order


# Select Item to Cart
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")  # used in get_total_cost() method
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f' item #{self.id}'

    def get_cost(self):
        return self.price * self.quantity
