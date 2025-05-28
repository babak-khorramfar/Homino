from django.urls import path
from .views import create_service_request

urlpatterns = [
    path("request/", create_service_request, name="create_service_request"),
    path("request/", create_service_request),
]
