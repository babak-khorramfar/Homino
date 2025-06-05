from django.urls import path
from services.api_views import (
    CategoryListView,
    ServiceListView,
    ServiceRequestCreateView,
)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("", ServiceListView.as_view(), name="service-list"),
    path("request/create/", ServiceRequestCreateView.as_view(), name="create-request"),
]
