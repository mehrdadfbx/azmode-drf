from django.urls import path
from .views import AdminCreateUserView

urlpatterns = [
    path('create-user/', AdminCreateUserView.as_view(), name='admin-create-user'),
]