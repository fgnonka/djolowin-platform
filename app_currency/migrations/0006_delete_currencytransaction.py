# Generated by Django 4.1.7 on 2023-04-18 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_currency', '0005_alter_currencypackage_purchases'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CurrencyTransaction',
        ),
    ]
