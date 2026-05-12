"""
Smart Tourism — Custom Permission Classes
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Only admin users (is_staff or role==admin) may access."""
    message = "Only administrators can perform this action."

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_staff or getattr(request.user, 'role', '') == 'admin')
        )


class IsVisitor(BasePermission):
    """Only visitors (role==visitor) may access."""
    message = "Only visitors can perform this action."

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            getattr(request.user, 'role', '') == 'visitor'
        )


class IsAdminOrReadOnly(BasePermission):
    """Admins have full access; everyone else read-only."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_staff or getattr(request.user, 'role', '') == 'admin')
        )


class IsOwnerOrAdmin(BasePermission):
    """Object-level: owner or admin."""
    message = "You do not have permission to access this resource."

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or getattr(request.user, 'role', '') == 'admin':
            return True
        # obj.user or obj.visitor
        owner = getattr(obj, 'user', None) or getattr(obj, 'visitor', None)
        return owner == request.user


class IsAuthenticatedOrReadOnly(BasePermission):
    """Authenticated users have full access; anonymous users read-only."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)