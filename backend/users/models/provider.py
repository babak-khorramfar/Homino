from django.db import models
from django.conf import settings
from django.utils import timezone


class ProviderProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="provider_profile",
    )
    bio = models.TextField(blank=True)
    national_id = models.CharField(max_length=20, blank=True)  # کد ملی
    profile_image = models.ImageField(
        upload_to="profiles/providers/", blank=True, null=True
    )

    # وضعیت فعال بودن یا تایید
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)  # آیا الان سفارش می‌پذیرد

    # تاریخ‌ها
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return f"Provider: {self.user.full_name}"
