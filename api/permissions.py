from rest_framework import permissions

class IsOwnerOfApproval(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user making the request is the owner of the approval
        return obj.users == request.user
    