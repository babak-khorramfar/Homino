from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from services.models import ServiceRequest, Proposal, Message, Review
from common.models import ActivityLog, Attachment
import os


@receiver(post_save, sender=ServiceRequest)
def log_service_request(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            user=instance.customer, action="create_service_request"
        )


@receiver(post_save, sender=Proposal)
def log_proposal(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(user=instance.provider, action="submit_proposal")


@receiver(post_save, sender=Message)
def log_message(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(user=instance.sender, action="send_message")


@receiver(post_save, sender=Review)
def log_review(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(user=instance.customer, action="submit_review")


@receiver(post_delete, sender=Attachment)
def delete_attachment_file(sender, instance, **kwargs):
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)
