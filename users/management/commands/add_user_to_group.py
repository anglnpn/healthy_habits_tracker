from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from users.models import User


class Command(BaseCommand):
    """
    Команда для добавления пользователя в группу
    """

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='id пользователя')
        parser.add_argument('group', type=str, help='название группы пользователей')

    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']
        group_name = kwargs['group']

        user = User.objects.get(pk=user_id)
        group = Group.objects.get(name=group_name)

        user.groups.add(group)
