from django.urls import path
from services.api_views import CategoryListView, ServiceListView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("services/", ServiceListView.as_view(), name="service-list"),
]
