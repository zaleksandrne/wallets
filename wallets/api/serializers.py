from rest_framework import serializers

from .models import Exchange, Wallet, Transaction


class WalletSerializerRead(serializers.ModelSerializer):
    balance = serializers.FloatField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Wallet


class WalletSerializerWrite(serializers.ModelSerializer):
    currency = serializers.ChoiceField(
        choices = Wallet.CHOICES,
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

    class Meta:
        fields = '__all__'
        model = Exchange