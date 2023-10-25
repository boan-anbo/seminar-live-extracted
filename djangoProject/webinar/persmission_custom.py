from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from djangoProject import settings
from djangoProject.userprofile.actions import get_profile_by_user
from djangoProject.userprofile.models import UserProfile
from djangoProject.webinar.models import Webinar


class IsWebinarTagger(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            profile = get_object_or_404(UserProfile, user=request.user)
            if profile.isTagger:
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


    # def has_object_permission(self, request, view, obj: Webinar):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # Instance must have an attribute named `owner`.


class IsRecommender(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            profile = get_object_or_404(UserProfile, user=request.user)
            if profile.isRecommender:
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


    # def has_object_permission(self, request, view, obj: Webinar):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # Instance must have an attribute named `owner`.
class IsDirectPoster(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            profile = get_object_or_404(UserProfile, user=request.user)
            if profile.isDirectPoster:
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


    # def has_object_permission(self, request, view, obj: Webinar):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # Instance must have an attribute named `owner`.
