from django_filters import rest_framework as filters

from djangoProject.webinar_stat.models import WebinarStat


class WebinarStatFilter(filters.FilterSet):

    class Meta:
        model = WebinarStat
        fields = ['views']