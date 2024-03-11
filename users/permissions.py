from rest_framework.permissions import BasePermission


class IsUser(BasePermission):
    """
    Право доступа к редактированию/полному просмотру своего профиля
    """
    def has_permission(self, request, view):
        if request.user.id == view.get_object().id:
            return True
        else:
            return False
