from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import User
from catalog.models import Product, ProductCategory
from inventory.models import StockMovement
from .models import Order


class OrderTestBase(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username='customer', password='pass1234', phone='09120000000'
        )
        self.admin = User.objects.create_user(
            username='admin', password='pass1234', phone='09120000001', is_admin=True
        )
        self.category = ProductCategory.objects.create(name='cat')
        self.product = Product.objects.create(
            name='p1', price=1000, description='d', category=self.category, stock=10
        )

    def submit(self, items, user=None):
        self.client.force_authenticate(user=user or self.customer)
        return self.client.post(reverse('submit-order'), {'items': items}, format='json')

    def set_status(self, order_id, new_status, user=None):
        self.client.force_authenticate(user=user or self.admin)
        return self.client.patch(
            reverse('update-order-status', args=[order_id]),
            {'status': new_status},
            format='json',
        )

    def stock(self):
        self.product.refresh_from_db()
        return self.product.stock


class SubmitOrderTests(OrderTestBase):
    def test_submit_reduces_stock_and_logs_movement(self):
        response = self.submit([{'product_id': self.product.id, 'quantity': 2}])

        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.stock(), 8)
        movement = StockMovement.objects.get(product=self.product)
        self.assertEqual(movement.quantity_change, -2)
        self.assertIn(str(response.data['id']), movement.reason)

    def test_order_more_than_stock_is_accepted_and_stock_goes_negative(self):
        response = self.submit([{'product_id': self.product.id, 'quantity': 15}])

        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.stock(), -5)

    def test_duplicate_items_are_all_deducted(self):
        response = self.submit([
            {'product_id': self.product.id, 'quantity': 3},
            {'product_id': self.product.id, 'quantity': 4},
        ])

        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.stock(), 3)
        self.assertEqual(StockMovement.objects.filter(product=self.product).count(), 2)

    def test_unknown_product_returns_400_and_creates_nothing(self):
        response = self.submit([
            {'product_id': self.product.id, 'quantity': 2},
            {'product_id': 999999, 'quantity': 1},
        ])

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(StockMovement.objects.count(), 0)
        self.assertEqual(self.stock(), 10)

    def test_unauthenticated_user_cannot_submit(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            reverse('submit-order'),
            {'items': [{'product_id': self.product.id, 'quantity': 1}]},
            format='json',
        )
        self.assertEqual(response.status_code, 401)


class UpdateOrderStatusTests(OrderTestBase):
    def make_order(self, quantity=2):
        response = self.submit([{'product_id': self.product.id, 'quantity': quantity}])
        return response.data['id']

    def test_reject_restores_stock_and_logs_positive_movement(self):
        order_id = self.make_order(2)
        self.assertEqual(self.stock(), 8)

        response = self.set_status(order_id, 'rejected')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.stock(), 10)
        self.assertTrue(
            StockMovement.objects.filter(product=self.product, quantity_change=2).exists()
        )

    def test_reject_twice_does_not_restore_stock_twice(self):
        order_id = self.make_order(2)
        self.set_status(order_id, 'rejected')

        response = self.set_status(order_id, 'rejected')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.stock(), 10)

    def test_approved_order_cannot_be_rejected(self):
        order_id = self.make_order(2)
        self.set_status(order_id, 'approved')

        response = self.set_status(order_id, 'rejected')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.stock(), 8)

    def test_approve_does_not_change_stock(self):
        order_id = self.make_order(2)

        response = self.set_status(order_id, 'approved')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.stock(), 8)

    def test_non_admin_cannot_change_status(self):
        order_id = self.make_order(2)

        response = self.set_status(order_id, 'rejected', user=self.customer)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.stock(), 8)

    def test_reject_order_whose_product_was_deleted(self):
        order_id = self.make_order(2)
        self.product.delete()