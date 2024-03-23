from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import CreateUserView, MeView

urlpatterns = [
    path("users/", CreateUserView.as_view(), name="register"),
    path("users/me/", MeView.as_view(), name="me"),
    path("users/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

app_name = "books"
