from django.shortcuts import render
from cart.cart import Cart
from orders.models import OrderItem
from orders.forms import OrderCreateForm

from orders.tasks import order_created


def order_create(request):
    cart = Cart(request)  # from context_processor

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()

            for item in cart:
                # this method creates instances of the class OrderItem inside the cart
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price'],
                )
            cart.clear()

            # async
            order_created.delay(order.id)  # worker will take info about the order for sending email

            return render(
                request,
                'orders/order/order_success.html',
                {'order': order},
            )

    else:
        form = OrderCreateForm()
        return render(
            request,
            'orders/order/order_create.html',
            {'cart': cart, 'form': form}
        )
