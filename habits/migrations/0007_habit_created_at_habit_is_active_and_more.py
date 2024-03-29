# Generated by Django 4.2.10 on 2024-03-07 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0006_alter_habit_periodicity'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='habit',
            name='is_active',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Активность'),
        ),
        migrations.AddField(
            model_name='habit',
            name='last_date_worked',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Дата последнего оповещения'),
        ),
        migrations.AddField(
            model_name='habit',
            name='telegram_chat_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Telegram'),
        ),
    ]
