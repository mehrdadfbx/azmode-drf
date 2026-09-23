from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from accounts.permissions import IsAdmin
from catalog.models import Product
from .models import Order, OrderItem
from .serializers import OrderCreateSerializer, OrderSerializer, UpdateOrderStatusSerializer



class UpdateOrderStatusView(UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = UpdateOrderStatusSerializer
    permission_classes = [IsAdmin]
    http_method_names = ['patch']

class SubmitOrderView(APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        items_data = serializer.validated_data['items']

        requested_totals_by_product = {}
        for item in items_data:
            product_id = item['product_id']
            quantity = item['quantity']
            requested_totals_by_product[product_id] = requested_totals_by_product.get(product_id, 0) + quantity

        with transaction.atomic():
            products_locked = {}
            for product_id, requested_qty in requested_totals_by_product.items():
                try:
                    product = Product.objects.select_for_update().get(id=product_id)
                except Product.DoesNotExist:
                    raise ValidationError(f'محصول با شناسه {product_id} دیگر در فروشگاه موجود نیست.')

                if product.stock < requested_qty:
                    raise ValidationError(
                        f'موجودی کالا {product.name} کافی نیست (درخواست: {requested_qty}، موجود: {product.stock}).'
                    )

                products_locked[product_id] = product

            # ساخت سفارش
            order = Order.objects.create(
                user=request.user,
                customer_name=request.user.username,
                customer_phone=request.user.phone,
                status='pending',
            )

            # ساخت آیتم‌های سفارش + کم کردن موجودی
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

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class MyOrdersView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user)


class AllOrderView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAdmin]
    queryset = Order.objects.all()