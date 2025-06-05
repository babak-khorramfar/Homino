from django.db import models
from django.conf import settings
from services.models import ServiceRequest
from django.utils import timezone


class Review(models.Model):
    request = models.OneToOneField(
        ServiceRequest, on_delete=models.CASCADE, related_name="review"
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="given_reviews"
    )
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_reviews",
    )

    # امتیازهای تفکیکی
    punctuality = models.PositiveSmallIntegerField()
    behavior = models.PositiveSmallIntegerField()
    quality = models.PositiveSmallIntegerField()

    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("request", "customer")

    def average_rating(self):
        return round((self.punctuality + self.behavior + self.quality) / 3, 2)

    def __str__(self):
        return (
            f"Review {self.average_rating()}⭐️ by {self.customer} for {self.provider}"
        )
