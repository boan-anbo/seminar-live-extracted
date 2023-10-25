from django_filters import rest_framework as filters

from djangoProject.report.models import Report


class ReportFilter(filters.FilterSet):

    class Meta:
        model = Report
        fields = ['type']