# Create your views here.
from django_filters import rest_framework as filters
from rest_framework import viewsets

from djangoProject.link.filters import LinkFilter
from djangoProject.link.models import Link
from djangoProject.link.serializers import LinkSerializer


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class=LinkFilter
