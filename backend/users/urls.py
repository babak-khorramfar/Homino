from django.urls import path
from users.api_views import (
    LogoutRealView,
    SignupView,
    LoginView,
    MeView,
    UpdateCustomerProfileView,
    UpdateProviderProfileView,
    LogoutView,
    ProviderSkillListView,
    ProviderSkillUpdateView,
    SendOTPView,
    VerifyOTPView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("provider/skills/", ProviderSkillListView.as_view(), name="provider-skills"),
    path("logout/real/", LogoutRealView.as_view(), name="logout-real"),
    path("auth/send-otp/", SendOTPView.as_view(), name="send-otp"),
    path("auth/verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path(
        "provider/skills/update/",
        ProviderSkillUpdateView.as_view(),
        name="update-provider-skills",
    ),
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
