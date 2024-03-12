from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.apps import ApiConfig
from api.views import MyObtainTokenPairView

app_name = ApiConfig.name


urlpatterns = [
    path('', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

