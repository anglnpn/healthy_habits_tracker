# Generated by Django 4.2.10 on 2024-03-07 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0008_alter_habit_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habit',
            name='last_date_worked',
        ),
        migrations.AddField(
            model_name='habit',
            name='date_worked',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Дата следующего оповещения'),
        ),
    ]