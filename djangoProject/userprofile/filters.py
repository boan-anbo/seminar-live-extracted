from django_filters import rest_framework as filters

from djangoProject.userprofile.models import UserProfile


class UserProfileFilter(filters.FilterSet):

    class Meta:
        model = UserProfile
        fields = ['id']