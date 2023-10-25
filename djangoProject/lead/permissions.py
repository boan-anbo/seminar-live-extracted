from django.shortcuts import get_object_or_404
from rest_framework import permissions

from djangoProject.userprofile.models import UserProfile


class LeadPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_superuser
        elif view.action in ['create']:
            profile = get_object_or_404(UserProfile, user=request.user)
            if profile.isDirectPoster:
                return True
            return request.user.is_superuser
        elif view.action == 'destroy':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update']:
            return request.user.is_superuser
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        # everyone can view webinar instance detail
        if view.action == 'retrieve':
            return True
        # only admin can update, partial_update, or destorp the instance.
        elif view.action in ['update', 'partial_update', 'destroy']:
            profile = get_object_or_404(UserProfile, user=request.user)
            if profile.isDirectPoster:
                return True

            return request.user.is_superuser
        # elif view.action == 'destroy':
        #     # return request.user.is_superuser
        #     return request.user.is_superuser
        else:
            return False



class IsLeadCollector(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            profile = get_object_or_404(UserProfile, user=request.user)
            if profile.isLeadCollector:
                return True
            else:
                return False
            # print(userProfile.user.id)
            # if userProfile.isTagger == True:
            # return False
            # else:
            # return False
        except:
            raise

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
