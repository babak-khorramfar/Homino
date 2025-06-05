from rest_framework.exceptions import PermissionDenied


def require_role(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated or request.user.role != role:
                raise PermissionDenied(
                    f"شما مجاز به استفاده از این سرویس نیستید ({role})"
                )
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
