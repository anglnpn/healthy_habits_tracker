from datetime import datetime

from django.shortcuts import render
from rest_framework import generics

from config.settings import TELEGRAM_BOT_API_TOKEN
from habits.models import Habit
from habits.paginators import HabitsPagination
from rest_framework.permissions import IsAuthenticated, AllowAny

from habits.permissions import IsAuthorHabit, IsModer
from habits.serializers import HabitSerializer, HabitPublicUsefulListSerializer, HabitPublicPleasantListSerializer
from habits.services import calculate_next_notification_time

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class HabitCreateAPIView(generics.CreateAPIView):
    """
    Создание привычки
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        # Установка пользователя перед сохранением
        serializer.save(user=self.request.user)

        # Получение ID созданной привычки
        habit_id = serializer.instance.id
        print(habit_id)
        habit = Habit.objects.get(id=habit_id)
        # Установка даты и времени создания привычки
        time = habit.time
        periodicity = habit.periodicity
        notification_time = datetime.utcnow()

        next_notification_time = calculate_next_notification_time(time, periodicity, notification_time)
        print(next_notification_time)

        habit.notification_time = next_notification_time
        habit.save()
        print(type(habit.notification_time))
        # Или можно получить ID привычки из сохраненного объекта
        # habit_id = serializer.data.get('id')


class HabitListAPIView(generics.ListAPIView):
    """
    Просмотр списка привычек
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitsPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(user=self.request.user)


class HabitUsefulListAPIView(generics.ListAPIView):
    """
    Просмотр списка полезных публичных привычек
    """
    serializer_class = HabitPublicUsefulListSerializer
    queryset = Habit.objects.filter(pleasant_habit=False)
    pagination_class = HabitsPagination
    permission_classes = [IsAuthenticated]


class HabitPleasantListAPIView(generics.ListAPIView):
    """
    Просмотр списка приятных публичных привычек
    """
    serializer_class = HabitPublicPleasantListSerializer
    queryset = Habit.objects.filter(pleasant_habit=True)
    pagination_class = HabitsPagination
    permission_classes = [IsAuthenticated]


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """
    Просмотр привычки
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated, IsAuthorHabit | IsModer]


class HabitDeleteAPIView(generics.DestroyAPIView):
    """
    Удаление привычки
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorHabit]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """
    Изменение привычки
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorHabit | IsModer]


class GetChatId(APIView):
    """
    Контроллер для упрощенного получения chat_id
    и записи в привычки
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        global telegram_user_id
        bot_token = TELEGRAM_BOT_API_TOKEN
        url = f'https://api.telegram.org/bot{bot_token}/getUpdates'

        user_id = request.user.id

        print(user_id)

        try:
            response = requests.get(url)
            response_data = response.json()
            results_data = response_data['result']

            for result in results_data:
                if result.get('message'):
                    telegram_user_id = result['message']['chat']['id']

                    print(telegram_user_id)
                elif result.get('my_chat_member'):
                    telegram_user_id = result['my_chat_member']['chat']['id']

                    print(telegram_user_id)

            habits = Habit.objects.filter(user=user_id).all()
            for habit in habits:
                habit.telegram_chat_id = telegram_user_id
                print(habit.telegram_chat_id)
                habit.save()

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


