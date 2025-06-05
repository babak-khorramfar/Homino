from django.db import models
from django.conf import settings
from services.models import ServiceRequest


class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ("user", "کاربر"),
        ("request", "سفارش"),
        ("other", "متفرقه"),
    ]

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports_made"
    )
    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports_received",
    )
    request = models.ForeignKey(
        ServiceRequest, on_delete=models.SET_NULL, null=True, blank=True
    )
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Report by {self.reporter} - type: {self.report_type}"
