from django.contrib import admin
from django.urls import path, include
from services.views import home, register
from django.contrib.auth import views as auth_views
from services.views import CustomLoginView
from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):
    logout(request)
    return redirect("login")


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("register/", register, name="register"),  # مسیر ثبت‌نام
    path("services/", include("services.urls")),
    path(
        "login/",
        CustomLoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", logout_view, name="logout"),
]
