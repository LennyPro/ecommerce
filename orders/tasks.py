from celery import shared_task
from django.core.mail import send_mail
from orders.models import Order

'''
@shared_task
decorator that marks the following function as a shared task with "worker".
Used with Celery, a distributed task queue, allowing the function to be executed asynchronously 
by a worker process.
This makes function a task.
Inside orders/views.py we add the line of code "order_created.delay(order.id)" 
because this action is asynchronous. 
'''


@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order # {order.id}'
    message = f'Hello, {order.first_name} {order.last_name}, \n\n' \
              f'You have successfully placed an order.' \
              f'Delivery to {order.address} \n\n' \
 \
        # sends the email using Django's "send_mail" function
    mail_sent = send_mail(
        subject,
        message,
        from_email='admin@e_commerce.com',  # base email
        recipient_list=[order.email],  # list containing the recipient's email address
    )

    return mail_sent


'''Определяя задачи в tasks.py, вы можете разгружать долгосрочные или ресурсоемкие операции с помощью Celery,
 что улучшает отзывчивость и производительность вашего приложения Django. 

 Эти задачи могут ставиться в очередь, 
 планироваться и выполняться в фоновом режиме рабочими процессами Celery.'''
