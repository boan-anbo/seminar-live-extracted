# Create your views here.
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from djangoProject.webinar_stat.filters import WebinarStatFilter
from djangoProject.webinar_stat.models import WebinarStat
from djangoProject.webinar_stat.serializers import WebinarStatSerializer


class WebinarStatViewSet(viewsets.ModelViewSet):
    queryset = WebinarStat.objects.all().order_by('views')
    serializer_class = WebinarStatSerializer
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ('title',)
    filterset_class = WebinarStatFilter

    @action(detail=True, methods=['get'])
    def add_view(self,  request, pk=None):
        stat = WebinarStat.objects.get(pk=pk)
        # views = stat.views
        serializedStat = self.get_serializer(stat)
        return Response(serializedStat.data)

    @action(detail=True, methods=['get'])
    def reset_view(self, request, pk=None):
        stat = WebinarStat.objects.get(pk=pk)
        stat.views = 0
        serializedStat = self.get_serializer(stat)
        return Response(serializedStat.data)
