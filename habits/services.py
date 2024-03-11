from datetime import datetime, timedelta


def calculate_next_notification_time(time, periodicity, notification_time):
    """
    Функция принимает время, периодичность и время оповещения.
    Вычисляет и возвращает следующее время для оповещения.
    """
    # Преобразование предыдущей даты оповещения в объект datetime
    prev_not_datetime = notification_time

    # Вычисление следующей даты оповещения в соответствии с периодичностью
    next_not_date = prev_not_datetime + timedelta(days=periodicity)

    # Соединение следующей даты оповещения с временем оповещения
    next_not_datetime = datetime.combine(next_not_date, time)

    # Возвращаем следующую дату и время оповещения
    return next_not_datetime
