from django.contrib import admin
from .models import Product, ProductCategory, PackagingType
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(PackagingType)