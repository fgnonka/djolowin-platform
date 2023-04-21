# Generated by Django 4.1.7 on 2023-04-07 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playercard', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cardrarity',
            options={'ordering': ['name'], 'verbose_name': 'Card Rarity', 'verbose_name_plural': 'Card Rarities'},
        ),
        migrations.AlterField(
            model_name='playercard',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
