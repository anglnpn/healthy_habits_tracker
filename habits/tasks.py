import logging
from datetime import datetime

from celery import shared_task

from habits.bot import send_message
from habits.models import Habit
from habits.services import calculate_next_notification_time

logging.basicConfig(level=logging.DEBUG)


@shared_task
def send_telegram_message():
    """
    Периодическая задача для отправки уведомлений в Telegram
    пользователям, для напоминания о выполнении привычек.
    """
    # получаем полезные привычки у которых время оповещения
    # соответствует времени в now
    # id телеграм чата должно быть заполнено

    habits = Habit.objects.select_related('user').filter(
        notification_time=datetime.utcnow(),
        pleasant_habit=False,
        user__telegram_chat_id__isnull=False,
    ).all()

    if habits:
        for habit in habits:
            # если привычки есть - собираем сообщение пользователю
            time = habit.time
            periodicity = habit.periodicity
            notification_time = habit.notification_time

            chat_id = habit.user.telegram_chat_id

            # собираем сообщение
            message_text = _get_message_text(habit)

            try:
                # вызываем функцию отправки сообщения пользователю
                send_message(chat_id, message_text)

                logging.info(f"Сообщение отправлено - {chat_id}")
            except Exception as e:
                logging.warning(f"Ошибка при отправке {e}")

            # вызываем функцию подсчета времени следующего оповещения
            next_notification_time = calculate_next_notification_time(
                time, periodicity, notification_time
            )

            # устанавливаем вычисленное время
            habit.notification_time = next_notification_time
            # сохраняем изменения
            habit.save()

    else:
        logging.info("Привычек для оповещения нет")

    return 'Задача выполнена'


def _get_message_text(habit: Habit) -> str:
    if habit.related_habit:
        # если есть связанная приятная привычка
        message_text = f"Вам нужно выполнить привычку: " \
                       f"{habit.activity} в {habit.time} в {habit.location}" \
                       f"Время выполнения привычки: {habit.execution_time}" \
                       f"Ваше вознаграждение приятная привычка!" \
                       f"{habit.related_habit.activity} " \
                       f"в {habit.related_habit.time} " \
                       f"в {habit.related_habit.location}"

    else:
        # если нет связанной приятной привычки, берем вознаграждение
        message_text = f"Вам нужно выполнить привычку: " \
                       f"{habit.activity} в {habit.time} в {habit.location}" \
                       f"Время выполнения привычки: {habit.execution_time}" \
                       f"Вознаграждение за выполнение: {habit.award}"

    return message_text
