# Generated by Django 4.1.7 on 2023-05-17 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0007_auction_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='duration',
        ),
    ]