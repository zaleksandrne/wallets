# Generated by Django 3.0.5 on 2021-04-01 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_transaction_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wallet',
            options={'ordering': ['name'], 'verbose_name': 'Wallet', 'verbose_name_plural': 'Wallets'},
        ),
        migrations.AddField(
            model_name='transaction',
            name='description',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='api.Wallet', verbose_name='Wallet'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Wallet name'),
        ),
    ]
