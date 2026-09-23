from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import User
from catalog.models import Product, ProductCategory
from .models import StockMovement


class AdjustStockTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin', password='pass1234', phone='09120000001', is_admin=True
        )
        self.customer = User.objects.create_user(
            username='customer', password='pass1234', phone='09120000000'
        )
        category = ProductCategory.objects.create(name='cat')
        self.product = Product.objects.create(
            name='p1', price=1000, description='d', category=category, stock=10
        )

    def adjust(self, product_id, data, user=None):
        self.client.force_authenticate(user=user or self.admin)
        return self.client.post(
            reverse('adjust-stock', args=[product_id]), data, format='json'
        )

    def stock(self):
        self.product.refresh_from_db()
        return self.product.stock

    def test_positive_adjustment(self):
        response = self.adjust(self.product.id, {'quantity_change': 5, 'reason': 'رسید کالا'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['new_stock'], 15)
        self.assertEqual(self.stock(), 15)
        movement = StockMovement.objects.get(product=self.product)
        self.assertEqual(movement.quantity_change, 5)
        self.assertEqual(movement.reason, 'رسید کالا')

    def test_negative_adjustment_can_go_below_zero(self):
        response = self.adjust(self.product.id, {'quantity_change': -13, 'reason': 'خرابی'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.stock(), -3)

    def test_unknown_product_returns_404(self):
        response = self.adjust(999999, {'quantity_change': 1, 'reason': 'x'})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(StockMovement.objects.count(), 0)

    def test_missing_reason_returns_400_and_changes_nothing(self):
        response = self.adjust(self.product.id, {'quantity_change': 5})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.stock(), 10)
        self.assertEqual(StockMovement.objects.count(), 0)

    def test_non_admin_gets_403(self):
        response = self.adjust(
            self.product.id, {'quantity_change': 5, 'reason': 'x'}, user=self.customer
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.stock(), 10)

    def test_unauthenticated_gets_401(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            reverse('adjust-stock', args=[self.product.id]),
            {'quantity_change': 5, 'reason': 'x'},
            format='json',
        )

        self.assertEqual(response.status_code, 401)