from rest_framework import serializers

from .models import Exchange, Wallet, Transaction
from django.db.models.aggregates import Sum


class WalletSerializerRead(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()

    def get_balance(self, obj):
        transactions = obj.transactions.all().aggregate(
            Sum('value')).get('value__sum') or 0
        exchange_sent = obj.exchange_sent.all().aggregate(
            Sum('value')).get('value__sum') or 0
        exchange_taken = obj.exchange_taken.all().aggregate(
            Sum('converted_value')).get('converted_value__sum') or 0
        return transactions - exchange_sent + exchange_taken

    class Meta:
        fields = '__all__'
        model = Wallet


class WalletSerializerWrite(serializers.ModelSerializer):
    currency = serializers.ChoiceField(
        choices=Wallet.CHOICES,
        error_messages={
            'invalid_choice': f'Not a valid choice. Value must be '
                              f'in {*( x[0] for x in Wallet.CHOICES),}'
                              })

    class Meta:
        fields = '__all__'
        model = Wallet


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Transaction


class ExchangeSerializer(serializers.ModelSerializer):
    converted_value = serializers.FloatField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Exchange
