# Generated by Django 4.1.7 on 2023-05-06 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_customerevent_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Last login'),
        ),
    ]
