from datetime import datetime, timedelta


def calculate_next_notification_time(time, periodicity, notification_time):
    # Преобразование предыдущей даты оповещения в объект datetime
    previous_notification_datetime = notification_time

    # Вычисление следующей даты оповещения в соответствии с периодичностью
    next_notification_date = previous_notification_datetime + timedelta(days=periodicity)

    # Соединение следующей даты оповещения с временем оповещения
    next_notification_datetime = datetime.combine(next_notification_date, time)
    print(next_notification_datetime)
    # Возвращаем следующую дату и время оповещения
    return next_notification_datetime
