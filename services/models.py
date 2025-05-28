from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Category Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("offered", _("Offered")),
        ("accepted", _("Accepted")),
        ("completed", _("Completed")),
    ]

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="service_requests",
        verbose_name=_("Customer"),
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Service Category"),
    )
    city = models.CharField(max_length=100, verbose_name=_("City"))
    address = models.TextField(verbose_name=_("Address"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name=_("Status"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    def __str__(self):
        return f"{self.category} - {self.city} - {self.customer.username}"


class UserProfile(models.Model):
    class UserType(models.TextChoices):
        CUSTOMER = "customer", _("سفارش‌دهنده")
        PROVIDER = "provider", _("متخصص")

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    user_type = models.CharField(
        max_length=10, choices=UserType.choices, verbose_name=_("نوع کاربر")
    )
    phone = models.CharField(max_length=20, verbose_name=_("شماره تماس"), blank=True)
    city = models.CharField(max_length=50, verbose_name=_("شهر"), blank=True)
    address = models.TextField(verbose_name=_("آدرس"), blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
