# Create your views here.
from django_filters import rest_framework as filters
from rest_framework import viewsets

from djangoProject.talk.filters import TalkFilter
from djangoProject.talk.models import Talk
from djangoProject.talk.serializers import TalkSerializer


class TalkViewSet(viewsets.ModelViewSet):
    queryset = Talk.objects.all().order_by('title')
    serializer_class = TalkSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class=TalkFilter
