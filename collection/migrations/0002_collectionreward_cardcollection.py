# Generated by Django 4.1.7 on 2023-04-07 09:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('playercard', '0005_delete_cardcollection'),
        ('collection', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionReward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reward', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.collection')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CardCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playercard.playercard')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_collection', to='collection.collection')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_collection_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
