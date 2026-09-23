from rest_framework import serializers
from .models import StockMovement

class AdjustStockSerializer(serializers.Serializer):
    quantity_change = serializers.IntegerField()
    reason = serializers.CharField(max_length=255)