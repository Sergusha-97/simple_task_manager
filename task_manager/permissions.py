from rest_framework import permissions


class IsManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_manager()
        )


class IsTaskOwnerOrReadOnly(permissions.BasePermission):
    ALLOWED_ACTIONS = ('list', 'partial_update', 'retrieve', 'update')

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_manager():
            return True
        elif view.action in IsTaskOwnerOrReadOnly.ALLOWED_ACTIONS:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_superuser:
            return True
        elif obj.reporter == request.user:
            return True
        elif view.action in IsTaskOwnerOrReadOnly.ALLOWED_ACTIONS:
            return obj.executor == request.user


class IsSuperUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_superuser
        )
