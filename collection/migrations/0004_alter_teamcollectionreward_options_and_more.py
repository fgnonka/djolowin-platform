# Generated by Django 4.1.7 on 2023-04-13 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0003_masterteamcollection_masterteampositioncollection_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teamcollectionreward',
            options={'verbose_name_plural': 'Team rewards'},
        ),
        migrations.AlterModelOptions(
            name='teampositioncollectionreward',
            options={'verbose_name_plural': 'Team Position rewards'},
        ),
        migrations.RenameField(
            model_name='teamcollectionreward',
            old_name='reward',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='teampositioncollectionreward',
            old_name='reward',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='teamcollectionreward',
            name='collection',
        ),
        migrations.RemoveField(
            model_name='teamcollectionreward',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='teamcollectionreward',
            name='user',
        ),
        migrations.RemoveField(
            model_name='teampositioncollectionreward',
            name='collection',
        ),
        migrations.RemoveField(
            model_name='teampositioncollectionreward',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='teampositioncollectionreward',
            name='user',
        ),
        migrations.AddField(
            model_name='teamcollectionreward',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='teamcollectionreward',
            name='reward_type',
            field=models.CharField(choices=[('currency', 'In-App Currency'), ('rare_card', 'Rare Card')], default='currency', max_length=20),
        ),
        migrations.AddField(
            model_name='teamcollectionreward',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='teampositioncollectionreward',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='teampositioncollectionreward',
            name='reward_type',
            field=models.CharField(choices=[('currency', 'In-App Currency'), ('rare_card', 'Rare Card')], default='rare_card', max_length=20),
        ),
        migrations.AddField(
            model_name='teampositioncollectionreward',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
