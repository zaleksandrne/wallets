# Generated by Django 3.0.5 on 2021-04-16 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210415_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='currency',
            field=models.CharField(choices=[('rub', 'RUB'), ('usd', 'USD'), ('eur', ' EUR')], error_messages={'invalid_choice': 'My custom error'}, max_length=3),
        ),
    ]