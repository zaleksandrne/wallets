from rest_framework import serializers

from .models import Wallet, Transaction


class WalletSerializerRead(serializers.ModelSerializer):
    balance = serializers.FloatField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Wallet


class WalletSerializerWrite(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Wallet


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Transaction



