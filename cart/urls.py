from django.urls import path

from .views import (
    AddToCartView,
    CartListView,
    RemoveFromCartView,
    UpdateCartItemView,
)

urlpatterns = [
    path(''                ,CartListView.as_view()      ,name='cart-list'),
    path('add/'            ,AddToCartView.as_view()     ,name='cart-add'),
    path('<int:pk>/'       ,UpdateCartItemView.as_view(),name='cart-update',),
    path('<int:pk>/remove/',RemoveFromCartView.as_view(),name='cart-remove',),
]