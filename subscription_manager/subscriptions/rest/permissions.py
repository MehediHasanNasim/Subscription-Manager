from rest_framework import permissions

class IsAdminOrStaffCanManagePlan(permissions.BasePermission):
    """
    Admins can do anything.
    Staff can create/update/delete/view plans.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )


class IsAdminOrStaffReadOnly(permissions.BasePermission):
    """
    Only allow view access to staff or admin.
    No POST/PUT/DELETE.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        ) and request.method in permissions.SAFE_METHODS


class IsAdminOrOwnerForSubscriptions(permissions.BasePermission):
    """
    Admins/Staffs can access all.
    Users can only access their own subscriptions.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser or
            request.user.is_staff or
            obj.user == request.user
        )
