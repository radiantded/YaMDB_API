from rest_framework import permissions

from .models import ADMIN, MODERATOR


class IsAuthorOrModeratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or (
                request.user.is_authenticated
                and request.user.role == MODERATOR)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    request.user.role == ADMIN
                    or request.user.is_staff
                    or request.user.is_superuser
                ))
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.role == ADMIN
                or request.user.is_staff
                or request.user.is_superuser
            )
        )
