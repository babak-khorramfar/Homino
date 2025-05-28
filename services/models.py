from django.db import models
from django.contrib.auth.models import User


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار"),
        ("offered", "پیشنهاد دریافت شده"),
        ("accepted", "پذیرفته شده"),
        ("completed", "تکمیل شده"),
    ]

    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="service_requests"
    )
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.city} - {self.customer.username}"
