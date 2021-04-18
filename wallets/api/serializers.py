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
    wallet_name = serializers.SlugRelatedField(read_only=True,
                                               slug_field='name'
                                               )

    class Meta:
        fields = '__all__'
        model = Transaction


class ExchangeSerializer(serializers.ModelSerializer):
    converted_value = serializers.FloatField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Exchange


class ProfileSerializer(serializers.Serializer):
    total_balance = serializers.FloatField()
    currency = serializers.CharField()
