from rest_framework import serializers

from habits.models import Habit


class HabitCustomValidator:
    """
    Валидатор для приятной привычки
    """

    def __init__(self, pleasant_habit, periodicity,
                 execution_time, activity, award, related_habit):
        self.pleasant_habit = pleasant_habit
        self.periodicity = periodicity
        self.execution_time = execution_time
        self.activity = activity
        self.award = award
        self.related_habit = related_habit

    def __call__(self, value):

        pleasant_habit = dict(value).get(self.pleasant_habit)
        periodicity = dict(value).get(self.periodicity)
        execution_time = dict(value).get(self.execution_time)
        activity = dict(value).get(self.activity)
        award = dict(value).get(self.award)
        related_habit = dict(value).get(self.related_habit)

        if pleasant_habit is True:
            if periodicity is not None and execution_time is not None:
                raise serializers.ValidationError(
                    'Более чем одно поле из списка '
                    'обязательных полей "периодичность, '
                    'время выполнения, действие" были заполнены')
            elif execution_time is not None:
                raise serializers.ValidationError(
                    'Вы указали привычку приятной, '
                    'поле "время выполнения" должно быть пустым')
            elif activity is None:
                raise serializers.ValidationError(
                    'Вы указали привычку приятной, '
                    'заполните действие')
            elif periodicity is not None:
                raise serializers.ValidationError(
                    'Вы указали привычку приятной, '
                    'поле "периодичность" должно быть пустым')
            elif award is not None:
                raise serializers.ValidationError(
                    'Приятная привычка не может иметь вознаграждения')

            print("Приятная привычка была успешно добавлена")

        else:
            if periodicity is None:
                raise serializers.ValidationError(
                    "Вы указали привычку полезной, "
                    "заполните периодичность")
            elif execution_time is None:
                raise serializers.ValidationError(
                    "Вы указали привычку полезной, "
                    "заполните время выполнения")
            elif activity is None:
                raise serializers.ValidationError(
                    "Вы указали привычку полезной, "
                    "заполните действие")
            elif award is None and related_habit is None:
                raise serializers.ValidationError(
                    "У полезной привычки должно быть или"
                    "вознаграждение или связанная привычка")
            elif award is not None and related_habit is not None:
                raise serializers.ValidationError(
                    "У полезной привычки не может быть "
                    "и вознаграждения и связанной привычки")

            print("Полезная привычка была успешно добавлена")


class ExecutionTimeCustomValidator:
    """
    Валидатор для времени выполнения.
    Время должно быть не больше 120 секунд.
    """

    def __init__(self, execution_time):
        self.execution_time = execution_time

    def __call__(self, value):
        ex_time = dict(value).get(self.execution_time)
        if ex_time:
            total_seconds = ((ex_time.hour * 60 + ex_time.minute) * 60
                             + ex_time.second)

            if total_seconds > 120:
                raise serializers.ValidationError(
                    "Время выполнения должно быть не больше 120 секунд")


class PeriodicityCustomValidator:
    """
    Валидатор для периодичности привычки.
    Нельзя не выполнять привычку более 7 дней
    """

    def __init__(self, periodicity):
        self.periodicity = periodicity

    def __call__(self, value):
        periodicity = dict(value).get(self.periodicity)

        if periodicity:
            if periodicity > 7:
                raise serializers.ValidationError(
                    "Нельзя не выполнять привычку более 7 дней")
            elif periodicity < 1:
                raise serializers.ValidationError(
                    "Периодичность должна быть больше 0")


class RelatedHabitCustomValidator:
    """
    Валидатор для связанной привычки.
    """

    def __init__(self, related_habit):
        self.related_habit = related_habit

    def __call__(self, value):
        related_habit = dict(value).get(self.related_habit)
        if related_habit:
            habit_obj = Habit.objects.filter(
                id=related_habit.id,
                pleasant_habit=False)
            if habit_obj:
                raise serializers.ValidationError(
                    "Связанная привычка может быть только приятной")
