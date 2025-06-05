from django.urls import path
from users.api_views import (
    SignupView,
    LoginView,
    MeView,
    UpdateCustomerProfileView,
    UpdateProviderProfileView,
    LogoutView,
    ProviderSkillListView,
    ProviderSkillUpdateView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("provider/skills/", ProviderSkillListView.as_view(), name="provider-skills"),
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
