# Generated by Django 4.1.7 on 2023-06-05 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0008_remove_transaction_user_transaction_buyer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctiontransaction',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
