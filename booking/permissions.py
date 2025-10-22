from rest_framework import permissions

class IsAdminRole(permissions.BasePermission):
    """
    Custom permision check to only allow admin role users
    """
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", None) == 'admin'
        )