#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import permissions


class IsSupperUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user:
            return request.user.is_superuser
        return False


class IsStaffOrTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return view.action == 'retrieve' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
