from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class UserProfile(models.Model):
    class UserType(models.TextChoices):
        CUSTOMER = "customer", _("Customer")
        PROVIDER = "provider", _("Provider")

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    user_type = models.CharField(max_length=10, choices=UserType.choices)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"


class ServiceCategory(MPTTModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Parent Category",
    )

    class MPTTMeta:
        order_insertion_by = ["title"]

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.title


class UserService(models.Model):
    provider = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="services"
    )
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    experience_years = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.provider.username} - {self.category.title}"


class ServiceRequest(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", _("Pending")
        OFFERED = "offered", _("Offered")
        ACCEPTED = "accepted", _("Accepted")
        COMPLETED = "completed", _("Completed")
        CANCELED = "canceled", _("Canceled")

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
    scheduled_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.category} - {self.city} - {self.customer.username}"


class Proposal(models.Model):
    service_request = models.ForeignKey(
        ServiceRequest, on_delete=models.CASCADE, related_name="proposals"
    )
    provider = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="proposals"
    )
    price_estimate = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Proposal by {self.provider.username} for {self.service_request}"


class Review(models.Model):
    service_request = models.ForeignKey(
        ServiceRequest, on_delete=models.CASCADE, related_name="reviews"
    )
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews_given"
    )
    provider = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews_received"
    )
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} → {self.provider.username} ({self.rating})"


class ChatMessage(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"


class SupportTicket(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", _("Open")
        CLOSED = "closed", _("Closed")
        IN_PROGRESS = "in_progress", _("In Progress")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="support_tickets"
    )
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.OPEN
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.subject}"
