from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class UserTestCase(APITestCase):
    """
    Тестирование работы с пользователем.
    """

    def setUp(self) -> None:
        self.user = User.objects.create(
            name='Test',
            surname='Test',
            email='test5@t.com',
            is_superuser=True)

    def test_create_user(self):
        """
        Тестирование создания пользователя
        """

        data = {
            "password": "testtestpassword",
            "name": "Test",
            "surname": "Test",
            "age": 20,
            "email": "test9@t.com",
            "phone": "83939303033",
            "city": "Test"
        }

        response_create = self.client.post(
            '/user/create/',
            data=data
        )

        self.assertEqual(
            response_create.status_code,
            status.HTTP_201_CREATED
        )
        # Проверяем, что пользователь действительно создан
        created_user = User.objects.get(email='test9@t.com')
        self.assertIsNotNone(created_user)

    def test_list_user(self):
        """
        Тестирование просмотра списка пользователей
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            '/user/list/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    #

    def test_retrieve_user(self):
        """
        Тестирование просмотра одного пользователя
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            f'/user/{self.user.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_user(self):
        """
        Тестирование изменения пользователя
        """
        data = {
            "name": "test7499",
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            f'/user/update/{self.user.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_user(self):
        """
        Тестирование удаление пользователя
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            f'/user/delete/{self.user.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            User.objects.filter(id=self.user.id).exists()
        )
