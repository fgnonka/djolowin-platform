# Generated by Django 4.1.7 on 2023-06-05 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0011_remove_auction_unique_auction_auction_unique_auction'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]