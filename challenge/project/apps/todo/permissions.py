from rest_framework.permissions import IsAuthenticated


class UserPermissions(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user
