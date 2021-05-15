import os, requests

from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Sum
from rest_framework import mixins, status, views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, SAFE_METHODS

from .models import Exchange, Wallet
from .serializers import (ExchangeSerializer, TransactionSerializer,
                          WalletSerializerRead, WalletSerializerWrite,
                          ProfileSerializer)


APIKEY = os.environ.get('APIKEY')
APIURL = os.environ.get('APIURL')


class BaseViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,):
    pass


class WalletViewSet(BaseViewSet,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    queryset = Wallet.objects.all()
    permission_classes = [AllowAny, ]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return WalletSerializerRead
        return WalletSerializerWrite

    def perform_create(self, serializer):
        serializer.save(balance=0)


class TransactionViewSet(BaseViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        wallet = get_object_or_404(Wallet, id=self.kwargs.get('id'))
        return wallet.transactions.all()

    def perform_create(self, serializer):
        wallet = get_object_or_404(Wallet, id=self.kwargs.get('id'))
        serializer.save(wallet=wallet)
        wallet.balance += serializer.validated_data.get('value')
        wallet.save()


def get_exchange_rate(s_currency, r_currency):
    s_currency, r_currency = s_currency.upper(), r_currency.upper()
    data = {'q': f'{s_currency}_{r_currency}',
                'compact': 'ultra',
                'apiKey': APIKEY
                }
    rate = requests.get(APIURL, data)
    rate = rate.json().get(f'{s_currency}_{r_currency}')
    return rate


class ExchangeViewSet(BaseViewSet):
    queryset = Exchange.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = ExchangeSerializer

    def perform_create(self, serializer):
        sender = serializer.validated_data.get('sender')
        recipient = serializer.validated_data.get('recipient')
        s_currency, r_currency = sender.currency, recipient.currency
        rate = get_exchange_rate(s_currency, r_currency)
        value = serializer.validated_data['value']
        converted_value = value * rate
        serializer.save(converted_value=converted_value)
        sender.balance -= value
        recipient.balance += converted_value
        sender.save()
        recipient.save()


class ProfileView(views.APIView):
    def get(self, request):
        currency = request.query_params.get('currency') or 'rub'
        if currency not in (x[0] for x in Wallet.CHOICES):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        wallets = Wallet.objects.all()
        totals = wallets.values('currency').annotate(balance=Sum('balance'))
        total_balance = sum(
            subsum['balance'] * get_exchange_rate(
                subsum['currency'], currency) for subsum in totals)
        data = {'total_balance': total_balance, 'currency': currency}
        serializer = ProfileSerializer(data)
        return Response(serializer.data)
