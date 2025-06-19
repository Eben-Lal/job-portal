from rest_framework import permissions


class IsEmployerOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow GET, HEAD, OPTIONS for all authenticated users
        return hasattr(request.user, 'employer_profile') and obj.employer == request.user.employer_profile
