# Generated by Django 4.2.10 on 2024-03-13 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram_chat_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Telegram'),
        ),
    ]
