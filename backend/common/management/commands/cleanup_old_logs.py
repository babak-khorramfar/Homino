from django.core.management.base import BaseCommand
from common.models import ActivityLog
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = "پاکسازی لاگ‌های قدیمی‌تر از ۶۰ روز"

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(days=60)
        deleted_count, _ = ActivityLog.objects.filter(created_at__lt=cutoff).delete()
        self.stdout.write(self.style.SUCCESS(f"{deleted_count} لاگ قدیمی حذف شد."))
