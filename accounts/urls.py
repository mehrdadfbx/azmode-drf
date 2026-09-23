from django.urls import path
from .views import AdminCreateUserView, UserInfoView

urlpatterns = [
    path('create-user/', AdminCreateUserView.as_view(), name='admin-create-user'),
    path('me/',          UserInfoView.as_view()       , name='user_informations')
]