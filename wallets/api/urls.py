from django.urls import include, path
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import ExchangeViewSet, WalletViewSet, TransactionViewSet

router = DefaultRouter()

router.register('wallets', WalletViewSet)
router.register(r'wallets/(?P<id>\d+)/transactions',
                TransactionViewSet,
                basename='transactions'
                )
router.register('exchanges',
                ExchangeViewSet,
                basename='exchanges'
                )                
schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/redoc/',
         schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
