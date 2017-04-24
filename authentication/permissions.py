from rest_framework import permissions


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user:
            return obj == request.user
        return False


class IsSupperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            return request.user.is_superuser
        return False


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            return request.user.is_authenticated()
        if 'user' in request.session:
            return True
        return False
