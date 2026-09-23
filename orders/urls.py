from django.urls import path
from .views import AllOrderView, MyOrdersView, SubmitOrderView, UpdateOrderStatusView

urlpatterns = [
    path('submit/',          SubmitOrderView.as_view()      , name='submit-order'),
    path('mine/',            MyOrdersView.as_view()         , name='my-orders'),
    path('<int:pk>/status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('',                 AllOrderView.as_view()         , name='all-orders'),
]