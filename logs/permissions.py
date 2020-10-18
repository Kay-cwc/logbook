from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    '''
    custom permission that allows the user create an entry edit it
    '''

    def has_object_permission(self, request, view, obj):
        '''
        read is alloed to any request
        so GET, HEAD, OPTIONS requests are allowed
        '''
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.created_by == request.user:
            access_right = True

        return access_right
