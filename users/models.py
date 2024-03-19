from django.contrib.auth.models import AbstractUser
from django.db import models

from config.utils import NULLABLE


class User(AbstractUser):
    """
    Модель для создания пользователя.
    Создается при регистрации.
    """
    username = None
    name = models.CharField(max_length=50, verbose_name='имя')
    surname = models.CharField(max_length=50, verbose_name='фамилия')
    age = models.IntegerField(verbose_name='возраст', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='media/',
                               verbose_name='аватар',
                               **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='город', **NULLABLE)
    telegram_chat_id = models.IntegerField(
        verbose_name='Telegram',
        **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
