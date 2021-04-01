from django.db import models


class Wallet(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Wallet name',
                            unique=True,
                            )

    class Meta:
        ordering = ['name']
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'


class Transaction(models.Model):
    value = models.FloatField(max_length=200,
                              verbose_name='value(rub)')
    wallet = models.ForeignKey(Wallet,
                               on_delete=models.CASCADE,
                               related_name='transactions',
                               verbose_name='Wallet'
                               )
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    description = models.CharField(max_length=300,
                                   null=True,
                                   blank=True,
                                   verbose_name='Description')

    class Meta:
        ordering = ['date']
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'


