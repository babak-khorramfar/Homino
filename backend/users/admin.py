from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("phone", "full_name", "role", "is_active", "created_at")
    search_fields = ("phone", "full_name")
