# Generated by Django 4.1.7 on 2023-04-24 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0003_auction_watchers'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='auction_ended',
            field=models.BooleanField(default=False),
        ),
    ]
