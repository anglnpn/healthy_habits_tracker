from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя
    """
    class Meta:
        model = User
        fields = '__all__'


class LimitedUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя, вывод только определенных полей
    """

    class Meta:
        model = User
        fields = [
            'name',
            'age',
            'avatar',
            'city']
