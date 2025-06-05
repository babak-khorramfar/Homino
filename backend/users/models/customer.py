from django.db import models
from django.conf import settings
from django.utils import timezone


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile",
    )
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(
        upload_to="profiles/customers/", blank=True, null=True
    )

    # تاریخ‌ها
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return f"Customer: {self.user.full_name}"
