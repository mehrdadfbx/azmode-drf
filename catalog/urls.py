from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, PackagingTypeViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'packaging-types', PackagingTypeViewSet)

urlpatterns = router.urls