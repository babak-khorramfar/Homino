from django.urls import path
from .views import register, service_list, request_list, create_service_request

urlpatterns = [
    path("categories/", service_list, name="service_list"),
    path("requests/", request_list, name="request_list"),
    path("requests/new/", create_service_request, name="create_service_request"),
]
