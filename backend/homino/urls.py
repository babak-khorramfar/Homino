from django.contrib import admin
from django.urls import path, include
from services.views import home, login_view, register, CustomLoginView
from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):
    logout(request)
    return redirect("login")


urlpatterns = [
    # صفحات عمومی و auth
    path("", include("services.urls")),  # splash, home, categories, ...
    path("home/", home, name="home"),
    path("admin/", admin.site.urls),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    # اگر نیاز به custom login class داشته باشید:
    # path("login/", CustomLoginView.as_view(), name="login"),
    path("", include("pwa.urls")),
    path("api/", include("services.api_urls")),
]
