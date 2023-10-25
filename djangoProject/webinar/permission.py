from rest_framework import permissions

from djangoProject import settings


class WebinarPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if settings.DEBUG:
            return True

        if view.action == 'list' or view.action == 'create':
            return request.user.is_authenticated and request.user.is_superuser
        elif view.action in ['retrieve']:
            return True
        elif view.action in ['update', 'partial_update', 'destroy']:
            return False
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        # everyone can view webinar instance detail
        if view.action == 'retrieve':
            return True
        # only admin can update, partial_update, or destorp the instance.
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_superuser
        # elif view.action == 'destroy':
        #     # return request.user.is_superuser
        #     return request.user.is_superuser
        else:
            return False

