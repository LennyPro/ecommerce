from django.test import TestCase
from inventory.models import Category


class CategoryTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Pizza', slug='pizza')
        self.category1 = Category.objects.create(name='Burgers', slug='burgers')
        self.category2 = Category.objects.create(name='Drinks', slug='drinks')

    def test_ordering_by_name_version1(self):
        categories = list(Category.objects.all())
        print(f'test1 categories: {categories}')
        self.assertEqual(categories[0].name, 'Burgers')
        self.assertEqual(categories[1].name, 'Drinks')
        self.assertEqual(categories[2].name, 'Pizza')

    def test_ordering_by_name_version2(self):
        expected_order = ['Burgers', 'Drinks', 'Pizza']
        actual_order = list(Category.objects.values_list('name', flat=True))
        print(f' test2 actual order: {actual_order}')
        self.assertEqual(actual_order, expected_order)
