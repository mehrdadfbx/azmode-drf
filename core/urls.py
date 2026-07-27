from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/',      include('accounts.urls')),
    path('api/',              include('catalog.urls')),
    path('api/orders/',       include('orders.urls')),
    path('api/cart/',         include('cart.urls')),
    path('api/notification/', include('notification.urls')),
    path('api/inventory/',    include('inventory.urls')),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)