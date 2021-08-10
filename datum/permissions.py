from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'create']:
            return request.user.is_staff
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'update', 'destroy']:
            return obj.user == request.user or request.user.is_staff

        return False

class MatchAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_staff
        elif view.action in ['list', 'retrieve']:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['list', 'retrieve']:
            return obj.current_user == request.user or request.user.is_staff
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_staff
            
        return False

class UserAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'list']:
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'delete', 'destroy']:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'update', 'partial_update', 'delete', 'destroy']:
            return obj == request.user or request.user.is_staff

        return False
<<<<<<< HEAD

class InterestAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_staff
        elif view.action in ['list', 'retrieve']:
            return request.user.is_authenticated
        return False
=======
>>>>>>> 4f5bcd5439ce6912781b008a9d58e2e2de0b1a5c
