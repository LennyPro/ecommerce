from django.urls import path, include
from cart import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>', views.cart_remove, name='cart_remove'),
]


'''The actual path defined in urlpatterns is not directly visible in the front-end templates. 
Instead, Django uses named URL patterns and the {% url %} template tag to dynamically generate the URLs. 
This abstraction allows for more maintainable and flexible code, 
as changes to URL patterns do not require updates to every template where the URL is used.'''
 