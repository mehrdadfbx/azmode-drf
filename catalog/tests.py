from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import User
from .models import Product, ProductCategory


class ProductStockVisibilityTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin', password='pass1234', phone='09120000001', is_admin=True
        )
        category = ProductCategory.objects.create(name='cat')
        self.product = Product.objects.create(
            name='p1', price=1000, description='d', category=category, stock=10
        )

    def test_anonymous_does_not_see_stock_fields(self):
        response = self.client.get(reverse('product-list'))

        self.assertEqual(response.status_code, 200)
        item = response.data['results'][0]
        self.assertNotIn('stock', item)
        self.assertNotIn('is_available', item)

    def test_admin_sees_stock_fields(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('product-list'))

        item = response.data['results'][0]
        self.assertIn('stock', item)
        self.assertIn('is_available', item)

    def test_admin_cannot_change_stock_through_product_patch(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            reverse('product-detail', args=[self.product.id]),
            {'stock': 999},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 10)