from django.urls import path
from services.api_views import CategoryListView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
]
