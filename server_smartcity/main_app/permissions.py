from rest_framework import permissions

class IsOwnerAndDraftOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if getattr(view, 'action', None) == 'create' and request.user.is_admin:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_admin:
            if request.method == 'PATCH':
                return (
                    obj.can_update_status(request.user)
                    and set(request.data.keys()) == {'status'}
                    and request.data.get('status') == obj.next_workflow_status()
                )
            return False

        if request.method == 'DELETE':
            return obj.can_delete(request.user)

        if request.method in ['PUT', 'PATCH']:
            requested_status = request.data.get('status', obj.Status.DRAFT)
            return (
                obj.can_edit(request.user)
                and requested_status in [obj.Status.DRAFT, obj.Status.REPORTED]
            )

        return False
