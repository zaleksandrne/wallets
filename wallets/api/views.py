import os, requests
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, SAFE_METHODS
from .models import Exchange, Wallet
from .serializers import (ExchangeSerializer, TransactionSerializer,
                          WalletSerializerRead, WalletSerializerWrite)

from dotenv import load_dotenv

load_dotenv()

APIKEY = os.getenv('APIKEY')
APIURL = os.getenv('APIURL')


class BaseViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,):
    pass


class WalletViewSet(BaseViewSet, mixins.UpdateModelMixin):
    queryset = Wallet.objects.all()
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
    permission_classes = [AllowAny, ]
    serializer_class = ExchangeSerializer

    def perform_create(self, serializer):
        s_currency = serializer.validated_data.get('sender').currency
        r_currency = serializer.validated_data.get('recipient').currency
        s_currency, r_currency = s_currency.upper(), r_currency.upper()
        data = {'q': f'{s_currency}_{r_currency}',
                'compact': 'ultra',
                'apiKey': APIKEY
                }
        rate = requests.get(APIURL, data)  # getting the exchange rate
        rate = rate.json().get(f'{s_currency}_{r_currency}')
        serializer.save(
            converted_value=serializer.validated_data['value'] * rate)
