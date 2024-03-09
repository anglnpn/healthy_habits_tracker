from django.urls import path
from habits.apps import HabitsConfig
from habits.views import HabitCreateAPIView, HabitListAPIView, HabitRetrieveAPIView, HabitUpdateAPIView, \
    HabitDeleteAPIView, HabitUsefulListAPIView, HabitPleasantListAPIView, HabitAddTelegramID

app_name = HabitsConfig.name

urlpatterns = [
    path('create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('list/', HabitListAPIView.as_view(), name='habit_list'),
    path('list_useful/', HabitUsefulListAPIView.as_view(), name='habit_list_useful'),
    path('list_pleasant/', HabitPleasantListAPIView.as_view(), name='habit_list_pleasant'),
    path('habit/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_get'),
    path('update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('delete/<int:pk>/', HabitDeleteAPIView.as_view(), name='habit_delete'),
    path('add_telegram_id/', HabitAddTelegramID.as_view(), name='habit_add_telegram_id'),

]
