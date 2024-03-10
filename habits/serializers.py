from rest_framework import serializers

from habits.models import Habit
from habits.validators import HabitCustomValidator, ExecutionTimeCustomValidator, PeriodicityCustomValidator, \
    RelatedHabitCustomValidator


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для полезной/приятной привычки
    """

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [HabitCustomValidator('pleasant_habit', 'periodicity', 'execution_time', 'activity',
                                           'award', 'related_habit'),
                      ExecutionTimeCustomValidator('execution_time'),
                      PeriodicityCustomValidator('periodicity'),
                      RelatedHabitCustomValidator('related_habit')]


class HabitPublicUsefulListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка публичных полезных привычек
    """

    class Meta:
        model = Habit
        fields = ['id', 'location', 'time', 'activity', 'periodicity', 'award']


class HabitPublicPleasantListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка публичных приятных привычек
    """

    class Meta:
        model = Habit
        fields = ['id', 'location', 'time', 'activity']
