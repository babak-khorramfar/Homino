from django.urls import path
from . import views

urlpatterns = [
    path("", views.service_list, name="service_list"),  # نمایش لیست سرویس‌ها
    path("requests/", views.request_list, name="request_list"),
]
