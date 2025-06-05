from django.db import models
from django.conf import settings
from django.utils import timezone
from models import ServiceRequest


class Proposal(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار تأیید"),
        ("accepted", "پذیرفته‌شده"),
        ("rejected", "ردشده"),
        ("canceled", "لغوشده توسط متخصص"),
    ]

    request = models.ForeignKey(
        ServiceRequest, on_delete=models.CASCADE, related_name="proposals"
    )
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_proposals",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        unique_together = (
            "request",
            "provider",
        )  # جلوگیری از ارسال چندباره برای یک سفارش

    def __str__(self):
        return f"Proposal by {self.provider.full_name} for {self.request.id}"
