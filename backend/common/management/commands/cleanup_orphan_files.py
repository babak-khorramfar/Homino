from django.core.management.base import BaseCommand
from common.models import Attachment
import os


class Command(BaseCommand):
    help = "حذف فایل‌های ضمیمه‌ای که object اصلی آن‌ها دیگر وجود ندارد (orphan)"

    def handle(self, *args, **options):
        deleted_count = 0

        for attachment in Attachment.objects.all():
            try:
                # تلاش برای دسترسی به object مرتبط
                _ = attachment.content_object
            except attachment.content_type.model_class().DoesNotExist:
                if attachment.file and os.path.isfile(attachment.file.path):
                    os.remove(attachment.file.path)
                attachment.delete()
                deleted_count += 1

        self.stdout.write(self.style.SUCCESS(f"{deleted_count} فایل orphan حذف شد."))
