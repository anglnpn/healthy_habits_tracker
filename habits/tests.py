from datetime import datetime, timedelta
import unittest

from rest_framework.test import APITestCase
from rest_framework import status

from freezegun import freeze_time

from habits.services import calculate_next_notification_time
from habits.tasks import send_telegram_message
from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            name='Test',
            surname='Test',
            email='test@t.com',
            is_superuser=True)

        self.user_2 = User.objects.create(
            name='Test2',
            surname='Test2',
            email='test2@t.com',
            is_superuser=False)

        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            location='проверка локации',
            time='00:00:00',
            activity='поесть',
            pleasant_habit=True,
            publicity=False,
            telegram_chat_id=704348791)

        self.public_habit = Habit.objects.create(
            user=self.user,
            location='проверка локации',
            time='00:00:00',
            activity='поесть',
            pleasant_habit=True,
            publicity=True,
            telegram_chat_id=704348791)

    def test_create_useful_habit(self):
        """
        Тестирование создания полезной привычки
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'user': self.user.id,
            'location': 'проверка локации',
            'time': '00:00:00',
            'activity': 'проверка занятия',
            'periodicity': 1,
            'pleasant_habit': False,
            'award': 'проверка вознаграждения',
            'execution_time': '00:02:00',
            'publicity': False,
            'telegram_chat_id': 704348791
        }

        response = self.client.post(
            '/habit/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_create_pleasant_habit(self):
        """
        Тестирование создания приятной привычки
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'user': self.user.id,
            'location': 'проверка локации',
            'time': '00:00:00',
            'activity': 'проверка действия',
            'pleasant_habit': True,
            'publicity': False,
            'telegram_chat_id': 704348791
        }

        response = self.client.post(
            '/habit/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_habit_list(self):
        """
        Тестирование просмотра списка привычек
        """

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            '/habit/list/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_habit_list_useful(self):
        """
        Тестирование просмотра списка полезных привычек
        """

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            '/habit/list_useful/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_habit_list_pleasant(self):
        """
        Тестирование просмотра списка приятных привычек
        """

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            '/habit/list_pleasant/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_habit_id(self):
        """
        Тестирование просмотра привычки по ID
        """

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            f'/habit/{self.pleasant_habit.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_habit(self):
        """
        Тестирование изменения списка уроков
        """

        self.client.force_authenticate(user=self.user)

        data = {
            'user': self.user.id,
            'location': 'проверка локации 2',
            'time': '00:00:00',
            'activity': 'проверка действия 2',
            'pleasant_habit': True,
            'publicity': False,
            'telegram_chat_id': 704348791
        }

        response = self.client.put(
            f'/habit/update/{self.pleasant_habit.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_add_public_habit(self):
        """
        Тестирование добавление публичной привычки
        пользователю
        """
        self.client.force_authenticate(user=self.user_2)

        data = {
            'habit_id': self.public_habit.id,
        }

        response = self.client.post(
            '/habit/add_habit/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_delete_habit(self):
        """
        Тестирование удаление привычки
        """

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            f'/habit/delete/{self.pleasant_habit.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


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
        next_notification_time = calculate_next_notification_time(
            time, periodicity, notification_time)

        self.assertEqual(next_notification_time, expected_result)
