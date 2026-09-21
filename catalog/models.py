from django.db import models
from django.db.models import PROTECT

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PackagingType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    
class Product(models.Model):
    ASPECT_RATIO_CHOICES = [
    ('square', 'مربعی'),
    ('portrait', 'عمودی'),
    ('landscape', 'افقی'),
    ('tall', 'کشیده'),
    ]


    name               = models.CharField(max_length=255)
    price              = models.DecimalField(max_digits=12, decimal_places=2)
    description        = models.TextField()
    image              = models.ImageField(upload_to='product/', height_field=None, width_field=None, max_length=None)
    color              = models.JSONField(default=list,blank=True)
    size               = models.CharField(max_length=50, null=True, blank=True)
    brand              = models.CharField(max_length=50, null=True, blank=True)
    sku                = models.CharField(max_length=50, null=True, blank=True)
    specifications     = models.TextField(null=True, blank=True)
    stock              = models.PositiveIntegerField(default=0)
    image_aspect_ratio = models.CharField(
                            max_length=20,
                            choices=ASPECT_RATIO_CHOICES,
                            default='square',
                        )
    packaging_type      = models.ForeignKey(
                            PackagingType,
                            null=True,
                            blank=True,
                            on_delete=models.SET_NULL,
                            related_name='packing',
                        )
    category           = models.ForeignKey(
                            ProductCategory,
                            on_delete=models.PROTECT,
                            related_name='products'
                        )
    created_at          = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name