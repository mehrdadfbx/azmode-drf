from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from catalog.models import Product
from accounts.permissions import IsAdmin
from .models import StockMovement
from .serializers import AdjustStockSerializer


class AdjustStockView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, product_id):
        serializer = AdjustStockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity_change = serializer.validated_data['quantity_change']
        reason = serializer.validated_data['reason']

        with transaction.atomic():
            try:
                product = Product.objects.select_for_update().get(id=product_id)
            except Product.DoesNotExist:
                raise ValidationError('محصول پیدا نشد.')

            new_stock = product.stock + quantity_change
            if new_stock < 0:
                raise ValidationError('موجودی نمی‌تواند منفی شود.')

            product.stock = new_stock 
            product.save()

            StockMovement(self, *args, **kwargs)

            # این دو خط رو خودت بنویس:
            # ۱. product.stock رو به new_stock تغییر بده و save کن
            # ۲. یه StockMovement جدید بساز با product, quantity_change, reason

        return Response({'message': 'موجودی به‌روزرسانی شد.', 'new_stock': new_stock})