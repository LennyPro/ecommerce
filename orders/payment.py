from yookassa import Configuration, Payment
from django.conf import settings
import uuid

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


def create_payment(order):
    payment = Payment.create({
        "amount": {
            "value": str(order.get_total_cost()),
            "currency": "RUB",
        },
        "confirmation": {
            "type": "redirect",
            "return_url": settings.YOOKASSA_RETURN_URL,
        },
        "capture": True,  # instant payment if FALSE partial hold of funds
        "description": f"your order number is {order.id}",
    },
        uuid.uuid4()
    )
    return payment
