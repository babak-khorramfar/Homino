from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class ServiceCategory(MPTTModel):
    title = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="category_icons/", blank=True, null=True)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class MPTTMeta:
        order_insertion_by = ["title"]

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.title


class Service(models.Model):
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.CASCADE, related_name="services"
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
