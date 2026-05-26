from rest_framework import permissions

class IsOwnerAndDraftOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff:

            if request.method in ['PUT', 'PATCH']:
 
                return 'status' in request.data and len(request.data) == 1
            return False

        return obj.reporter == request.user and obj.status == 'DRAFT'
        return False