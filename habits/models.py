from django.db import models
from users.models import User
from config.utils import NULLABLE


class Habit(models.Model):
    """
    Модель для полезной и приятной привычки.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь')
    location = models.CharField(max_length=1000, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    activity = models.CharField(
        max_length=1000,
        verbose_name='Действие',
        **NULLABLE)
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Периодичность',
        **NULLABLE)
    pleasant_habit = models.BooleanField(
        default=False,
        verbose_name='Идентификатор приятной привычки')
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='Приятная привычка',
        **NULLABLE)
    award = models.CharField(
        max_length=1000,
        verbose_name='Вознаграждение',
        **NULLABLE)
    execution_time = models.TimeField(
        verbose_name='Время выполнения',
        **NULLABLE)
    publicity = models.BooleanField(
        default=False,
        verbose_name='Признак публичности')
    notification_time = models.DateTimeField(
        verbose_name='Дата и время следующего оповещения',
        **NULLABLE)

    class Meta:
        verbose_name = 'полезная/приятная привычка'
        verbose_name_plural = 'полезные/приятные привычки'
