# Generated by Django 2.1 on 2018-09-04 21:43

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ad_messages', '0006_favoritead'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FavoriteAd',
            new_name='FavouriteAd',
        ),
    ]
