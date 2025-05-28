from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    class UserType(models.TextChoices):
        CUSTOMER = "customer", _("Customer")
        PROVIDER = "provider", _("Provider")

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    user_type = models.CharField(max_length=10, choices=UserType.choices)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"


class ServiceCategory(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.title


class ServiceRequest(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", _("Pending")
        OFFERED = "offered", _("Offered")
        ACCEPTED = "accepted", _("Accepted")
        COMPLETED = "completed", _("Completed")

    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="service_requests"
    )
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.city} - {self.customer.username}"
