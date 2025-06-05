from django.urls import path
from users.api_views import (
    SignupView,
    LoginView,
    MeView,
    UpdateCustomerProfileView,
    UpdateProviderProfileView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
    path(
        "customer/profile/update/",
        UpdateCustomerProfileView.as_view(),
        name="update_customer_profile",
    ),
    path(
        "provider/profile/update/",
        UpdateProviderProfileView.as_view(),
        name="update_provider_profile",
    ),
]
