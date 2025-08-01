from django.contrib import admin
from inventory.models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # one element tuple must be followed by the comma


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'available', 'price', 'category',)
