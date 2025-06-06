import time
import logging
from django.db import connection

logger = logging.getLogger("slow_queries")


class SlowQueryLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        total_time = time.time() - start_time

        for query in connection.queries:
            duration = float(query.get("time", 0))
            if duration > 0.3:  # بیشتر از 300 میلی‌ثانیه
                logger.warning(
                    f"⏱️ Slow query detected ({duration:.3f}s): {query['sql'][:500]}"
                )

        return response
