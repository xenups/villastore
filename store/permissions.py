from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny


class IsLoggedInUserOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class IsAuthenticatedNotPost(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return False
        return super(IsAuthenticatedNotPost, self).has_permission(request, view)


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff
