#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import permissions
from django.contrib.auth.models import User


class IsSupperUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user:
            return request.user.is_superuser
        return False
