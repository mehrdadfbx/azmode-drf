from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework import filters

from .models import ProductCategory, Product, PackagingType
from .serializers import  PackagingTypeSerializer, ProductCategorySerializer, ProductSerializer, ProductPublicSerializer
from .permissions import IsAdminOrReadOnly

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields = [ 'category' ]
    search_fields    = ['name', 'description']

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated and user.is_admin:
            return ProductSerializer
        return ProductPublicSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class PackagingTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = PackagingType.objects.all()
    serializer_class = PackagingTypeSerializer