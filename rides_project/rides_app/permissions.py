from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    """
    Custom permission to only allow users with the 'admin' role to access the API.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == 'admin'