from django.db import models
from django.utils import timezone
from services.models import ServiceRequest
from django.conf import settings


class OrderStatus(models.Model):
    STATUS_CHOICES = [
        ("reserved", "رزرو شده"),
        ("accepted", "تأیید توسط متخصص"),
        ("started", "شروع به کار"),
        ("paused", "متوقف موقت"),
        ("finished", "اتمام کار"),
        ("canceled", "لغو شده"),
    ]

    request = models.OneToOneField(
        ServiceRequest, on_delete=models.CASCADE, related_name="order_status"
    )
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="active_orders"
    )

    current_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="reserved"
    )
    scheduled_time = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    note = models.TextField(blank=True)  # توضیح اختیاری برای وضعیت فعلی

    def mark_started(self):
        self.current_status = "started"
        self.started_at = timezone.now()
        self.save()

    def mark_finished(self):
        self.current_status = "finished"
        self.finished_at = timezone.now()
        self.save()

    def mark_canceled(self):
        self.current_status = "canceled"
        self.canceled_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.request} - {self.current_status}"
