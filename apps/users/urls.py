from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import (
    RegisterView,
    LoginView,
    ProfileView,
    CustomTokenRefreshView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('me/', ProfileView.as_view(), name='profile'),
]