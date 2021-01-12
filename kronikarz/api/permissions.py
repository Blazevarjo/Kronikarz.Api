from rest_framework import permissions


class IsEventOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.person.family_tree.user == request.user


class IsFamilyTreeOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsMariageOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.person_1.family_tree.user == request.user


class IsMediaOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.person.family_tree.user == request.user


class IsPersonOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.family_tree.user == request.user
