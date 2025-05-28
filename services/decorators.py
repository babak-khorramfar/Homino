from django.core.exceptions import PermissionDenied


def user_is_customer(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if (
            not request.user.is_authenticated
            or request.user.profile.user_type != "customer"
        ):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped_view
