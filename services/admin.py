from django.contrib import admin
from .models import UserProfile
from .models import ServiceCategory, ServiceRequest
from mptt.admin import DraggableMPTTAdmin


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(DraggableMPTTAdmin):
    pass


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("customer", "category", "city", "status", "created_at")
    list_filter = ("status", "city", "category")
    search_fields = ("customer__username", "city", "description")
    ordering = ("-created_at",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "user_type", "phone", "city")
