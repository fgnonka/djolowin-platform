# Generated by Django 4.1.7 on 2023-04-24 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0006_auctiontransaction_number_of_bids_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctiontransaction',
            name='number_of_watchers',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
