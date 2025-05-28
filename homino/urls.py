from django.contrib import admin
from django.urls import path, include
from services.views import home  # اگر صفحه اصلی هم از services میاد

urlpatterns = [
    path("", home, name="home"),  # فقط اگر نیاز داری home هم باشه
    path("admin/", admin.site.urls),
    path("register/", include("services.urls")),  # اگه فرم ثبت‌نام اونجاست
    path("services/", include("services.urls")),  # این لازمه برای حل مشکلت
]
