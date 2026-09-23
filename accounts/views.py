from rest_framework.generics import CreateAPIView

from .permissions import IsAdmin
from .serializers import AdminCreateUserSerializer


class AdminCreateUserView(CreateAPIView):
    serializer_class = AdminCreateUserSerializer
    permission_classes = [IsAdmin] 