from common.models import ActivityLog
from datetime import datetime


class ActivityLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and request.method in [
            "POST",
            "PUT",
            "DELETE",
        ]:
            path = request.path
            method = request.method
            action = f"{method} {path}"

            ActivityLog.objects.create(
                user=request.user,
                action=action,
                detail=f"درخواست {method} به مسیر {path} در {datetime.now()}",
            )

        return response
