from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response

from accounts.models import User

from .permissions import IsAdmin
from .serializers import AdminCreateUserSerializer, UserInfoSerializer


class AdminCreateUserView(CreateAPIView):
    serializer_class   = AdminCreateUserSerializer
    permission_classes = [IsAdmin] 


class UserInfoView(GenericAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    