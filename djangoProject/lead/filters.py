from django_filters import rest_framework as filters, DateFromToRangeFilter

from djangoProject.lead.models import Lead


class LeadFilter(filters.FilterSet):
    created = DateFromToRangeFilter()
    class Meta:
        model = Lead
        fields = ['created', 'status']