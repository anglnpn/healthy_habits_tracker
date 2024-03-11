from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    """
    Команда для создания группы модераторов
    """

    def add_arguments(self, parser):
        parser.add_argument('group_name', type=str, help='создание группы')

    def handle(self, *args, **kwargs):
        group_name = kwargs['group_name']

        moderator_group, created = Group.objects.get_or_create(name=group_name)

        if created:
            self.stdout.write(self.style.SUCCESS('Группа модераторов создана'))
        else:
            self.stdout.write(self.style.WARNING('Такая группа уже существует'))
