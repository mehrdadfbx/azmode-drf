from rest_framework import serializers

from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )

    product_image = serializers.ImageField(
        source="product.image",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "product_image",
            "quantity",
            "selected_color",
            "total_price",
        ]

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than 0"
            )

        return value