from django.db import models

from accounts.models import User
from catalog.models import Product


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    selected_color = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'product', 'selected_color',)

    def __str__(self):
        return self.product.name