# Generated by Django 4.2.10 on 2024-03-07 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0010_remove_habit_created_at_remove_habit_date_worked_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='telegram_chat_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Telegram'),
        ),
    ]