from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Read: allowed for any authenticated user.
    Write (PUT/PATCH/DELETE): only the owner of the task.
    """
    def has_object_permission(self, request, view, obj):
        # Safe methods are GET/HEAD/OPTIONS
        if request.method in SAFE_METHODS:
            return True
        # Owner check: task.user_id must equal current user's id
        return getattr(obj, "user_id", None) == getattr(request.user, "id", None)
