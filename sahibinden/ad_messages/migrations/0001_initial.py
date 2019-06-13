# Generated by Django 2.1 on 2018-08-26 23:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('price', models.IntegerField(default=1)),
                ('pub_date', models.DateField(default=django.utils.timezone.now, verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('sent_time', models.DateTimeField(auto_now=True)),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ad_messages.Ad')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ad_messages.User'),
        ),
        migrations.AddField(
            model_name='ad',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ad_messages.User'),
        ),
    ]
