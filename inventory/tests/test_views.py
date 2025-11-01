from django.test import TestCase
from inventory.models import Product, Category
from django.urls import reverse


class ProductListViewTest(TestCase):
    def setUp(self):
        # Teat table for TestCase
        self.category = Category.objects.create(name='Test-Category', slug='Test_Category')

        # Test object for test DB
        self.product1 = Product.objects.create(name='Pepperoni',
                                               slug='pepperoni',
                                               price=5.00,
                                               available=True,
                                               category=self.category)
        # Test object for test DB
        self.product2 = Product.objects.create(name='Margaritta',
                                               slug='margaritta',
                                               price=6.00,
                                               available=True,
                                               category=self.category)
        # Test object for test DB
        self.product3 = Product.objects.create(name='Burger',
                                               slug='burger',
                                               price=4.00,
                                               available=False,
                                               category=self.category)
        # Test URL
        self.url = reverse('inventory:product_list')

    def test_product_list_status_code_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        print(f'returned status code: {response.status_code}, expected: 200')
        self.assertTemplateUsed(response, 'inventory/product_list.html')

    def test_product_list_show_only_available_products(self):
        # GET request
        response = self.client.get(self.url)
        products = response.context['products']
        print(f'returned products: {products}')
        self.assertIn(self.product1, products)
        self.assertIn(self.product2, products)
        self.assertNotIn(self.product3, products)
