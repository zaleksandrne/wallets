# Generated by Django 3.0.5 on 2021-04-17 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='converted_value',
            field=models.FloatField(blank=True, max_length=200, null=True, verbose_name='Converted value'),
        ),
    ]
