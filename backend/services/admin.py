from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    ServiceCategory,
    ServiceRequest,
    Proposal,
    Review,
    ChatMessage,
    SupportTicket,
    Notification,
    UserService,
)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "parent")
    search_fields = ("title",)
    list_filter = ("parent",)


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("category", "city", "customer", "status", "created_at")
    search_fields = ("city", "description")
    list_filter = ("status", "category", "city")


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = (
        "service_request",
        "provider",
        "price_estimate",
        "is_accepted",
        "created_at",
    )
    list_filter = ("is_accepted", "created_at")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("customer", "provider", "rating", "created_at")
    list_filter = ("rating",)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "timestamp", "is_read")
    search_fields = ("sender__phone", "receiver__phone")


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ("user", "subject", "status", "created_at")
    list_filter = ("status",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "is_read", "created_at")
    list_filter = ("is_read",)


@admin.register(UserService)
class UserServiceAdmin(admin.ModelAdmin):
    list_display = (
        "provider",
        "category",
        "base_price",
        "experience_years",
        "is_verified",
    )
    list_filter = ("is_verified", "category")
