from datetime import datetime
import requests

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from config.settings import TELEGRAM_BOT_API_TOKEN
from habits.models import Habit
from habits.paginators import HabitsPagination
from habits.permissions import IsAuthorHabit, IsModer
from habits.serializers import (HabitSerializer,
                                HabitPublicUsefulListSerializer,
                                HabitPublicPleasantListSerializer)
from habits.services import calculate_next_notification_time


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

        habit = Habit.objects.get(id=habit_id)
        # Установка даты и времени привычки
        time = habit.time
        periodicity = habit.periodicity
        notification_time = datetime.utcnow()

        next_no_time = calculate_next_notification_time(
            time, periodicity, notification_time)

        habit.notification_time = next_no_time
        habit.save()


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
    queryset = Habit.objects.filter(pleasant_habit=False, publicity=True)
    pagination_class = HabitsPagination
    permission_classes = [IsAuthenticated]


class HabitPleasantListAPIView(generics.ListAPIView):
    """
    Просмотр списка приятных публичных привычек
    """
    serializer_class = HabitPublicPleasantListSerializer
    queryset = Habit.objects.filter(pleasant_habit=True, publicity=True)
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


class AddHabitToUserAPIView(generics.CreateAPIView):
    """
    Контроллер добавления публичной привычки
    к пользователю
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            # Получаем данные из запроса
            habit_id = request.data.get('habit_id')
            # Получаем пользователя из запроса
            user = request.user
            # Получаем публичную привычку по идентификатору
            public_habit = Habit.objects.get(id=habit_id)

            habit_values = public_habit.__dict__.copy()
            # Удаляем _state атрибут
            del habit_values['_state']
            # Удаляем 'id' из значений атрибутов,
            # чтобы не возникала конфликт с уже существующими объектами
            del habit_values['id']

            # Создаем новый объект Habit,
            # передавая значения атрибутов public_habit
            habit = Habit.objects.create(user=user, **habit_values)

            # Установка даты и времени привычки
            time = habit.time
            periodicity = habit.periodicity
            notification_time = datetime.utcnow()

            next_no_time = calculate_next_notification_time(
                time, periodicity, notification_time)

            habit.notification_time = next_no_time

            # Сохраняем привычку пользователю
            habit.save()

            # Сериализуем созданную привычку и возвращаем в ответе
            serializer = self.get_serializer(habit)

            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        except Habit.DoesNotExist:
            return Response({"error": "Публичная привычка не найдена."},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
