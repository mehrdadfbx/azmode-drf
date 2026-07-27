from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from .models import CartItem
from .serializers import CartItemSerializer


class AddToCartView(CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        selected_color = serializer.validated_data.get('selected_color')

        cart_item = CartItem.objects.filter(
            user=user,
            product=product,
            selected_color=selected_color
        ).first()

        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()

            serializer.instance = cart_item

        else:
            serializer.save(
                user=user
            )


class CartListView(ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(
            user=self.request.user
        )


class RemoveFromCartView(DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(
            user=self.request.user
        )


class UpdateCartItemView(UpdateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(
            user=self.request.user
        )