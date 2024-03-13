import requests

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import make_password

from config.settings import TELEGRAM_BOT_API_TOKEN
from users.models import User
from users.permissions import IsUser
from users.serializers import UserSerializer, LimitedUserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """
    Cоздание пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        # Хэширование пароля перед сохранением пользователя
        validated_data = serializer.validated_data
        password = validated_data.get('password')
        hashed_password = make_password(password)
        serializer.save(password=hashed_password)


class UserListAPIView(generics.ListAPIView):
    """
    Просмотр списка пользователей
    """
    queryset = User.objects.all()
    serializer_class = LimitedUserSerializer
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
    Просмотр одного пользователя
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return UserSerializer
        else:
            return LimitedUserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    Изменение пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUser]


class UserDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление пользователя
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUser]


class GetChatId(APIView):
    """
    Контроллер для упрощенного получения chat_id
    и записи в привычки
    """
    # serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        global telegram_user_id
        bot_token = TELEGRAM_BOT_API_TOKEN
        print(bot_token)
        url = f'https://api.telegram.org/bot{bot_token}/getUpdates'

        user_id = request.user.id
        print(user_id)

        try:
            response = requests.get(url)
            response_data = response.json()
            results_data = response_data['result']
            print(results_data)

            for result in results_data:
                if result.get('message'):
                    telegram_user_id = result['message']['chat']['id']

                    print(telegram_user_id)
                elif result.get('my_chat_member'):
                    telegram_user_id = result['my_chat_member']['chat']['id']

                    print(telegram_user_id)

            user = User.objects.get(id=user_id)
            user.telegram_chat_id = telegram_user_id
            user.save()
            print(user)

            return Response(f'id получен {telegram_user_id} и записан пользователю {user.id}', status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
