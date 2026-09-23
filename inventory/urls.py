from django.urls import path 
from .views import AdjustStockView

urlpatterns = [
    path('<int:product_id>/adjust/', AdjustStockView.as_view(),name='adjust-stock')
]
