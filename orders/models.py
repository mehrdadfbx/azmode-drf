from django.db import models

from accounts.models import User
from catalog.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار تایید'),
        ('approved', 'تایید شده'),
        ('rejected', 'رد شده'),
    ]

    user           = models.ForeignKey(User, on_delete=models.PROTECT)
    customer_name  = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=20)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.customer_name}"


class OrderItem(models.Model):
    order                 = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product               = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name_snapshot = models.CharField(max_length=255)
    unit_price_snapshot   = models.DecimalField(max_digits=12, decimal_places=2)
    quantity              = models.PositiveIntegerField()
    selected_color        = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.product_name_snapshot