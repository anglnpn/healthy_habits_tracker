from datetime import datetime, timedelta

from django.test import TestCase
import unittest
from freezegun import freeze_time

from habits.services import calculate_next_notification_time
from habits.tasks import send_telegram_message


class TestPeriodicTask(unittest.TestCase):
    """
    Тест для периодической задачи
    send_telegram_message
    """

    # замораживаем время
    @freeze_time("2024-03-10 00:00:00")
    def test_send_telegram_message(self):
        """
        Тест периодической задачи
        """

        result = send_telegram_message()
        expected_result = 'Задача выполнена'

        # проверка результата
        self.assertEqual(result, expected_result)


class TestCalculateNextTime(unittest.TestCase):
    """
    Тест для функции calculate_next_time
    """

    def test_calculate_next_time(self):
        """
        Тест функции calculate_next_time
        Функция должна правильно подсчитывать время
        следующего оповещения и возвращать его
        """
        time = datetime.utcnow().time()
        periodicity = 1
        notification_time = datetime.utcnow()
        exp_notification_date = notification_time + timedelta(days=periodicity)

        # Соединение следующей даты оповещения с временем оповещения
        expected_result = datetime.combine(exp_notification_date, time)

        # вызываем функцию
        next_notification_time = calculate_next_notification_time(time, periodicity, notification_time)

        self.assertEqual(next_notification_time, expected_result)
