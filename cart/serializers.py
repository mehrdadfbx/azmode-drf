from rest_framework import serializers

from .models import CartItem

class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'selected_color', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Quantity must be greater than 0'
            )

        return value