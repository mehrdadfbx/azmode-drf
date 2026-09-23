from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
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
                raise NotFound('محصول پیدا نشد.')

            new_stock = product.stock + quantity_change
            product.stock = new_stock
            product.save()

            StockMovement.objects.create(
                product=product,
                quantity_change=quantity_change,
                reason=reason,
            )

        return Response({'message': 'موجودی به‌روزرسانی شد.', 'new_stock': new_stock})