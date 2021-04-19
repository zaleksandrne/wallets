from django.db.models.fields import SlugField
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Exchange, Wallet, Transaction


class WalletSerializerRead(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Wallet


class WalletSerializerWrite(serializers.ModelSerializer):
    balance = serializers.FloatField(read_only=True)
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
    wallet = serializers.SlugRelatedField(read_only=True, slug_field='id')

    def validate(self, data):
        id = self.context.get('view').kwargs.get('id')
        wallet = get_object_or_404(Wallet, id=id)
        if wallet.balance + data.get('value') < 0:
            raise serializers.ValidationError('Balance is too low')
        return data

    class Meta:
        fields = '__all__'
        model = Transaction


class ExchangeSerializer(serializers.ModelSerializer):
    converted_value = serializers.FloatField(read_only=True)

    def validate(self, data):
        id = data.get('sender').id
        wallet = get_object_or_404(Wallet, id=id)
        if wallet.balance - data.get('value') < 0:
            raise serializers.ValidationError('Balance is too low')
        return data

    class Meta:
        fields = '__all__'
        model = Exchange


class ProfileSerializer(serializers.Serializer):
    total_balance = serializers.FloatField()
    currency = serializers.CharField()
