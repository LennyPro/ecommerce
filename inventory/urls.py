from django.urls import path
from inventory import views

app_name = 'inventory'

urlpatterns = [
    path('inventory/products', views.product_list, name='product_list'),
    path('inventory/<slug:category_slug>', views.product_list, name='product_list_by_category'),
    path('inventory/<int:product_id>/<slug:slug>', views.product_detail, name='product_detail'),
]