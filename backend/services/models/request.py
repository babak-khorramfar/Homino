from django.db import models
from django.conf import settings
from django.utils import timezone
from services.models import Service


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار بررسی"),
        ("accepted", "پذیرفته‌شده"),
        ("in_progress", "در حال انجام"),
        ("completed", "تکمیل‌شده"),
        ("canceled", "لغوشده"),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="service_requests",
    )
    service = models.ForeignKey(
        Service, on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.TextField(blank=True)
    location_text = models.TextField(blank=True)  # آدرس توصیفی
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    scheduled_time = models.DateTimeField(
        null=True, blank=True
    )  # برای زمان دلخواه مشتری
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return f"Request by {self.customer.full_name} for {self.service}"
