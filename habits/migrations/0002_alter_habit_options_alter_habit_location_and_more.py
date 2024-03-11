# Generated by Django 4.2.10 on 2024-03-04 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='habit',
            options={'verbose_name': 'полезная/приятная привычка', 'verbose_name_plural': 'полезные/приятные привычки'},
        ),
        migrations.AlterField(
            model_name='habit',
            name='location',
            field=models.CharField(max_length=1000, verbose_name='Место'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='time',
            field=models.TimeField(verbose_name='Время'),
        ),
    ]
