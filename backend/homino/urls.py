from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import logout
from django.shortcuts import redirect


urlpatterns = [
    path("api/users/", include("users.urls")),
    path("api/services/", include("services.urls")),
]
