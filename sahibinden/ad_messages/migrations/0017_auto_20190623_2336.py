# Generated by Django 2.1 on 2019-06-23 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ad_messages', '0016_auto_20190623_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='ad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages+', to='ad_messages.Ad'),
        ),
    ]
