from django.db import models


class Wallet(models.Model):
    CHOICES = (('rub', 'rub'), ('usd', 'usd'), ('eur', ' eur'))
    name = models.CharField(max_length=200,
                            verbose_name='Wallet name',
                            unique=True,
                            )
    currency = models.CharField(
        max_length=3,
        choices=CHOICES,
        )

    class Meta:
        ordering = ['name']
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'

    def __str__(self):
        return self.name


class Transaction(models.Model):
    value = models.FloatField(max_length=200,
                              verbose_name='Value')
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
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return str(self.value)


class Exchange(models.Model):
    value = models.FloatField(max_length=200,
                              verbose_name='Value')
    converted_value = models.FloatField(max_length=200,
                                        verbose_name='Converted value',
                                        null=True,
                                        blank=True)
    sender = models.ForeignKey(Wallet,
                               on_delete=models.CASCADE,
                               related_name='exchange_sent',
                               verbose_name='Sender'
                               )
    recipient = models.ForeignKey(Wallet,
                                  on_delete=models.CASCADE,
                                  related_name='exchange_taken',
                                  verbose_name='Recipient'
                                  )
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date')

    class Meta:
        ordering = ['date']
        verbose_name = 'Exchange'
        verbose_name_plural = 'Exchanges'

    def __str__(self):
        return f'{str(self.sender)}-->{str(self.recipient)}'
