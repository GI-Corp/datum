from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions, status
from django.core.exceptions import ValidationError
from datum.models import Match, Preference, Profile

class MatchAccessPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ['list', 'retrieve']:
            return obj.current_user == request.user or request.user.is_staff
        return False

class UserAccessPermission(permissions.BasePermission):
    # надо чтобы user вышел чтобы мог создать новый аккаунт
    def has_permission(self, request, view):
        if view.action == 'create':
            if request.user.is_authenticated:
                raise ValidationError(message='You have to sign out to register a new user.')
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['list', 'retrieve', 'update', 'partial_update',  'destroy']:
            return obj == request.user or request.user.is_staff
        return False

class InterestAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'list', 'update', 'partial_update', 'destroy']:
            return request.user.is_staff
        return True

class ProfileAccessPermission(permissions.BasePermission):
    # доступ к профилю если матчи совпали
    # убрать 
    def has_permission(self, request, view):
        if view.action in ['create', 'destroy']:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if view.action == 'update':
            return obj.user == request.user
        if view.action in ['list', 'retrieve']:
            return True
        return False

class PreferenceAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['list', 'retrieve', 'update', 'destroy']:
            return obj.user == request.user or request.user.is_staff
        return False