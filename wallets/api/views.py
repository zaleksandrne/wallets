from django.db.models import F
from django.db.models.aggregates import Sum
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, SAFE_METHODS
from .models import Exchange, Wallet
from .serializers import (ExchangeSerializer, TransactionSerializer, 
                          WalletSerializerRead, WalletSerializerWrite)


class BaseViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin):
    pass


class WalletViewSet(BaseViewSet):
    queryset = Wallet.objects.annotate(balance= Sum('transactions__value', distinct=True) - Sum('sent__value', distinct=True))
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


class ExchangeViewSet(BaseViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
    permission_classes = [AllowAny, ]