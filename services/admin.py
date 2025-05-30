from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import (
    UserProfile,
    ServiceCategory,
    ServiceRequest,
    UserService,
    Proposal,
    Review,
    ChatMessage,
    Notification,
    SupportTicket,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "user_type", "city", "phone")
    list_filter = ("user_type", "city")
    search_fields = ("user__username", "phone", "city")


admin.site.register(ServiceCategory, DraggableMPTTAdmin)


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("category", "city", "customer", "status", "created_at")
    list_filter = ("status", "city", "category")
    search_fields = ("customer__username", "city", "address")


@admin.register(UserService)
class UserServiceAdmin(admin.ModelAdmin):
    list_display = (
        "provider",
        "category",
        "base_price",
        "experience_years",
        "is_verified",
    )
    list_filter = ("category", "is_verified")
    search_fields = ("provider__username",)


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = (
        "service_request",
        "provider",
        "price_estimate",
        "is_accepted",
        "created_at",
    )
    list_filter = ("is_accepted",)
    search_fields = ("provider__username", "service_request__customer__username")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("customer", "provider", "rating", "created_at")
    search_fields = ("customer__username", "provider__username")


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "timestamp", "is_read")
    search_fields = ("sender__username", "receiver__username")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "is_read", "created_at")
    list_filter = ("is_read",)


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ("user", "subject", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("user__username", "subject")
