# Generated by Django 4.1.7 on 2023-04-06 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_currency', '0003_remove_currencytransaction_card_brand_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencytransaction',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
