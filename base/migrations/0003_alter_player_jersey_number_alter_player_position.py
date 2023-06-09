# Generated by Django 4.1.7 on 2023-04-09 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_team_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='jersey_number',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(choices=[('GK', 'Goalkeeper'), ('DEF', 'Defender'), ('MID', 'Midfielder'), ('FW', 'Forward')], max_length=3),
        ),
    ]
