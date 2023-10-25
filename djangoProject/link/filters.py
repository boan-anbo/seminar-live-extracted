from django_filters import rest_framework as filters

from djangoProject.link.models import Link


class LinkFilter(filters.FilterSet):

    class Meta:
        model = Link
        fields = ['type']