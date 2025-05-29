from django.contrib import admin
from django.urls import path, include
from services.views import home, login_view, register
from django.contrib.auth import views as auth_views
from services.views import CustomLoginView
from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):
    logout(request)
    return redirect("login")


urlpatterns = [
    path("", include("services.urls")),
    path("home/", home, name="home"),
    path("admin/", admin.site.urls),
    path("register/", register, name="register"),  # مسیر ثبت‌نام
    path("services/", include("services.urls")),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
