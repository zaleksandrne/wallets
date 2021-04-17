import json, os, requests

from rest_framework import serializers

from .models import Exchange, Wallet, Transaction
from django.db.models.aggregates import Sum

from dotenv import load_dotenv

load_dotenv()

APIKEY=os.getenv('APIKEY')
APIURL=os.getenv('APIURL')

class WalletSerializerRead(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()

    def get_balance(self, obj):
        transactions = obj.transactions.all().aggregate(
            Sum('value')).get('value__sum') or 0
        exchange_sent = obj.exchange_sent.all().aggregate(
            Sum('value')).get('value__sum') or 0
        exchange_taken = obj.exchange_taken.all().aggregate(
            Sum('value')).get('value__sum') or 0
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

class ExchangeSerializerWrite(serializers.ModelSerializer):
    converted_value = serializers.SerializerMethodField()

    def get_converted_value(self, obj):
        print(obj.sender.currency)
        s_currency = obj.sender.currency.upper()
        r_currency  = obj.recipient.currency.upper()
        data = {'q': f'{s_currency}_{r_currency}',
                'compact': 'ultra',
                'apiKey': APIKEY
                }
        rate = requests.get(APIURL, data).json().get(f'{s_currency}_{r_currency}')
        return obj.value * rate

    class Meta:
        fields = '__all__'
        model = Exchange
    
class ExchangeSerializerRead(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Exchange