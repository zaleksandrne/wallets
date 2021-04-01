from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import WalletViewSet, TransactionViewSet

router = DefaultRouter()

router.register('transactions', TransactionViewSet)
router.register('wallets', WalletViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
