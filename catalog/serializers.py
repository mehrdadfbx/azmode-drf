from rest_framework import serializers
from .models import PackagingType, Product, ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class PackagingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackagingType
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    packaging_type_name = serializers.CharField(source='packaging_type.name', read_only=True, allow_null=True)
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['stock']

    def get_is_available(self, obj):
        return obj.stock > 0

class ProductPublicSerializer(ProductSerializer):
    is_available = None

    class Meta(ProductSerializer.Meta):
        fields = None
        exclude = ['stock']