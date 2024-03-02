from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда для создания пользователя
    """
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin7@sky.pro',
            name='admin',
            surname='admin',
            is_staff=True,
            is_superuser=True

        )

        user.set_password('adas5678900')
        user.save()


