# Generated by Django 3.0.5 on 2021-04-15 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='currency',
            field=models.CharField(choices=[('rub', 'RUB'), ('usd', 'USD'), ('eur', ' EUR')], error_messages={'required': 'My custom error'}, max_length=3),
        ),
    ]