from django.urls import path
from users.api_views import SignupView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
]
