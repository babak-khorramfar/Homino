from django.urls import path
from users.api_views import SignupView, LoginView, MeView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
]
