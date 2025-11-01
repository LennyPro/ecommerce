import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

app = Celery('e_commerce_project')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_commerce_project.settings')

# redis config
app.conf.broker_url = os.getenv('CELERY_BROKER_URL')
app.conf.result_backend = os.getenv('CELERY_RESULT_BACKEND')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.worker_pool = "solo"
app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()

''' In summary, this script sets up and configures a Celery instance for a Django project, 
allowing it to handle asynchronous tasks and periodic scheduling.


if using RabbitMQ:
rabbitmq login on host 15672
http://localhost:15672/ '''
