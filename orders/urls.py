from django.urls import path
from .views import SubmitOrderView

urlpatterns = [
    path('submit/', SubmitOrderView.as_view(), name='submit-order'),
]