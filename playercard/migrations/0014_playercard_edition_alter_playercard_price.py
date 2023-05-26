# Generated by Django 4.1.7 on 2023-05-13 08:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playercard', '0013_rename_locked_playercard_is_locked'),
    ]

    operations = [
        migrations.AddField(
            model_name='playercard',
            name='edition',
            field=models.IntegerField(default=2024),
        ),
        migrations.AlterField(
            model_name='playercard',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(2000)]),
        ),
    ]