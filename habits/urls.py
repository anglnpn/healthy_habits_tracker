from django.urls import path

from habits.apps import HabitsConfig
from habits.views import (HabitCreateAPIView,
                          HabitListAPIView,
                          HabitRetrieveAPIView,
                          HabitUpdateAPIView,
                          HabitDeleteAPIView,
                          HabitUsefulListAPIView,
                          HabitPleasantListAPIView,
                          GetChatId,
                          AddHabitToUserAPIView)


app_name = HabitsConfig.name

urlpatterns = [
    path('create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('list/', HabitListAPIView.as_view(), name='habit_list'),
    path('list_useful/', HabitUsefulListAPIView.as_view(), name='list_useful'),
    path('list_pleasant/', HabitPleasantListAPIView.as_view(), name='list_pleasant'),
    path('<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_get'),
    path('update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('delete/<int:pk>/', HabitDeleteAPIView.as_view(), name='habit_delete'),
    path('get_chat_id/', GetChatId.as_view(), name='get_chat_id'),
    path('add_habit/', AddHabitToUserAPIView.as_view(), name='add_habit'),

]
