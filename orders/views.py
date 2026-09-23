from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsAdmin
from catalog.models import Product
from inventory.models import StockMovement
from .models import Order, OrderItem
from .serializers import OrderCreateSerializer, OrderSerializer, UpdateOrderStatusSerializer


class UpdateOrderStatusView(UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = UpdateOrderStatusSerializer
    permission_classes = [IsAdmin]
    http_method_names = ['patch']

    def perform_update(self, serializer):
        new_status = serializer.validated_data.get('status')

        with transaction.atomic():
            order = Order.objects.select_for_update().get(pk=serializer.instance.pk)

            if order.status != 'pending':
                raise ValidationError('وضعیت این سفارش دیگر قابل تغییر نیست.')

            serializer.save()

            if new_status == 'rejected':
                items = order.items.filter(product__isnull=False).order_by('product_id')
                for item in items:
                    product = Product.objects.select_for_update().get(pk=item.product_id)
                    product.stock += item.quantity
                    product.save()

                    StockMovement.objects.create(
                        product=product,
                        quantity_change=item.quantity,
                        reason=f'رد سفارش شماره {order.id}',
                    )


class SubmitOrderView(APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        items_data = serializer.validated_data['items']

        product_ids = sorted({item['product_id'] for item in items_data})

        with transaction.atomic():
            products_locked = {}
            for product_id in product_ids:
                try:
                    product = Product.objects.select_for_update().get(id=product_id)
                except Product.DoesNotExist:
                    raise ValidationError(f'محصول با شناسه {product_id} دیگر در فروشگاه موجود نیست.')
                products_locked[product_id] = product

            # ساخت سفارش
            order = Order.objects.create(
                user=request.user,
                customer_name=request.user.username,
                customer_phone=request.user.phone,
                status='pending',
            )

            # ساخت آیتم‌های سفارش + کم کردن موجودی + ثبت حرکت انبار
            for item in items_data:
                product = products_locked[item['product_id']]
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name_snapshot=product.name,
                    unit_price_snapshot=product.price,
                    quantity=item['quantity'],
                    selected_color=item.get('selected_color'),
                )

                product.stock -= item['quantity']
                product.save()

                StockMovement.objects.create(
                    product=product,
                    quantity_change=-item['quantity'],
                    reason=f'سفارش شماره {order.id}',
                )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyOrdersView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class AllOrderView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAdmin]
    queryset = Order.objects.all()