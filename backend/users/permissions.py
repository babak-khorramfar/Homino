from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "customer"


class IsProvider(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "provider"


class IsAdminOrSupport(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser


class IsAdminOrSupport(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or request.user.is_superuser)
        )


class IsRelatedToObject(BasePermission):
    """
    بررسی می‌کنه که آیا کاربر به object مربوط هست یا نه:
    - اگر object.customer == request.user
    - یا object.provider == request.user
    - یا object.sender == request.user
    - یا object.receiver == request.user
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        return any(
            [
                hasattr(obj, "customer") and obj.customer == user,
                hasattr(obj, "provider") and obj.provider == user,
                hasattr(obj, "sender") and obj.sender == user,
                hasattr(obj, "receiver") and obj.receiver == user,
            ]
        )
