# Generated by Django 4.1.7 on 2023-05-06 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_currency', '0006_delete_currencytransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='currencypackage',
            name='og_price',
            field=models.DecimalField(decimal_places=2, default=200, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='currencypackage',
            name='stripe_price',
            field=models.IntegerField(default=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='currencypackage',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]