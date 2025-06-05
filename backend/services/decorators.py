from django.http import HttpResponseForbidden
from functools import wraps


def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")
            if not hasattr(request.user, "profile"):
                return HttpResponseForbidden("User profile not found.")
            if request.user.profile.user_type != required_role:
                return HttpResponseForbidden("You are not allowed to access this page.")
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
