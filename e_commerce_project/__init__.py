# this file ensures that the Celery app is loaded when Django starts

from e_commerce_project.celery import app as celery_app
__all__ = ['celery_app']

'''
This setup ensures that whenever Django starts, 
the Celery app is also initialized and ready to handle tasks, 
maintaining a clean and clear import structure.
'''