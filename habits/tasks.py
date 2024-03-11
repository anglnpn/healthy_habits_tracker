from datetime import datetime
from celery import shared_task
from habits.bot import send_message
from habits.models import Habit
from habits.services import calculate_next_notification_time

import logging

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
    habits = Habit.objects.filter(notification_time=datetime.utcnow(),
                                  pleasant_habit=False,
                                  telegram_chat_id__isnull=False).all()
    if habits:
        for habit in habits:
            # если привычки есть - собираем сообщение пользователю
            related_habit = habit.related_habit
            chat_id = habit.telegram_chat_id
            activity = habit.activity
            time = habit.time
            location = habit.location
            award = habit.award
            execution_time = habit.execution_time
            periodicity = habit.periodicity
            notification_time = habit.notification_time
            if related_habit:
                # если есть связанная приятная привычка
                message_text = f"Вам нужно выполнить привычку: " \
                               f"{activity} в {time} в {location}" \
                               f"Время выполнения привычки: {execution_time}" \
                               f"Ваше вознаграждение приятная привычка!" \
                               f"{related_habit.activity} " \
                               f"в {related_habit.time} " \
                               f"в {related_habit.location}"

            else:
                # если нет связанной приятной привычки, берем вознаграждение
                message_text = f"Вам нужно выполнить привычку: " \
                               f"{activity} в {time} в {location}" \
                               f"Время выполнения привычки: {execution_time}" \
                               f"Вознаграждение за выполнение: {award}" \

            # вызываем функцию подсчета времени следующего оповещения
            next_notification_time = calculate_next_notification_time(
                time,
                periodicity,
                notification_time)

            # устанавливаем вычисленное время
            habit.notification_time = next_notification_time
            # сохраняем изменения
            habit.save()

            try:
                # вызываем функцию отправки сообщения пользователю
                send_message(chat_id, message_text)

                logging.info(f"Сообщение отправлено - {chat_id}")
            except Exception as e:
                logging.warning(f"Ошибка при отправке {e}")

    else:
        logging.info("Привычек для оповещения нет")

    return 'Задача выполнена'
