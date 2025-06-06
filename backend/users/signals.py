# services/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from users.models import CustomerProfile, ProviderProfile
import os


@receiver(post_delete, sender=CustomerProfile)
def delete_customer_image(sender, instance, **kwargs):
    if instance.profile_image and os.path.isfile(instance.profile_image.path):
        os.remove(instance.profile_image.path)


@receiver(post_delete, sender=ProviderProfile)
def delete_provider_image(sender, instance, **kwargs):
    if instance.profile_image and os.path.isfile(instance.profile_image.path):
        os.remove(instance.profile_image.path)
