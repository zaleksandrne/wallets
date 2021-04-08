from django.db.models.aggregates import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, SAFE_METHODS
from .models import Transaction, Wallet
from .serializers import (WalletSerializerRead, WalletSerializerWrite,
                          TransactionSerializer)


class BaseViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin):
    pass


class WalletViewSet(BaseViewSet):
    queryset = Wallet.objects.annotate(balance=Sum('transactions__value'))
    permission_classes = [AllowAny, ]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return WalletSerializerRead
        return WalletSerializerWrite


class TransactionViewSet(BaseViewSet):
    def get_queryset(self):
        wallet = get_object_or_404(Wallet, id=self.kwargs.get('id'))
        return wallet.transactions.all()
    
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['wallet', ]
