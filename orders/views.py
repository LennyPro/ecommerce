from django.shortcuts import render, redirect
from cart.cart import Cart
from orders.models import OrderItem, Order
from orders.forms import OrderCreateForm
from orders.tasks import order_created
from orders.payment import create_payment

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse


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

            # create payment
            payment = create_payment(order)  # from payment.py
            order.payment_id = payment.id
            order.save()

            # async
            # order_created.delay(order.id)  # worker will take info about the order for sending email

            # return render(
            #     request,
            #     'orders/order/order_success.html',
            #     {'order': order},
            # )

            # redirect customer straight to payment instead of success page:
            return redirect(payment.confirmation.confirmation_url)

    else:
        form = OrderCreateForm()
        return render(
            request,
            'orders/order/order_create.html',
            {'cart': cart, 'form': form}
        )


@csrf_exempt
@require_POST
def yookassa_webhook(request):
    event = json.loads(request.body.decode('utf-8'))  # create an event and deserialize it
    event_type = event.get('event')  # identify the kid of event type
    payment_id = event.get('object').get('id')  # extract event's id

    if event_type == 'payment.succeeded':
        order = Order.objects.get(payment_id=payment_id)  # from models.py class Order
        order.paid = True  # from model.py class Order change the status of payment
        order.status = 'completed'  # define the status of payment
        order.save()

    elif event_type == 'payment.canceled':
        order = Order.objects.get(payment_id=payment_id)
        order.paid = False
        order.status = 'canceled'
        order.save()

    return JsonResponse({'status': 'ok'})
