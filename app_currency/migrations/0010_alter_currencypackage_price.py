# Generated by Django 4.1.7 on 2023-05-13 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_currency', '0009_alter_currencypackage_stripe_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencypackage',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]