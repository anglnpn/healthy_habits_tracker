from datetime import datetime
from celery import shared_task
from habits.bot import send_message
from habits.models import Habit
from habits.services import calculate_next_notification_time


@shared_task
def send_telegram_message():
    """
    Фоновая асинхронная задача для отправки уведомлений в Telegram
    пользователям, для напоминания о выполнении привычек.
    """
    # получаем объект привычки
    habits = Habit.objects.filter(notification_time=datetime.utcnow(),
                                  telegram_chat_id__isnull=False).all()

    for habit in habits:
        if habit:
            chat_id = habit.telegram_chat_id
            activity = habit.activity
            time = habit.time
            location = habit.location
            award = habit.award
            execution_time = habit.execution_time
            periodicity = habit.periodicity
            notification_time = habit.notification_time

            message_text = f"Вам нужно выполнить привычку: " \
                           f"{activity} в {time} в {location}" \
                           f"Время выполнения привычки: {execution_time}" \
                           f"Вознаграждение за выполнение: {award}" \

            next_notification_time = calculate_next_notification_time(time, periodicity, notification_time)

            habit.notification_time = next_notification_time
            habit.save()

            send_message(chat_id, message_text)
        else:
            return "Нет привычек для оповещений"
