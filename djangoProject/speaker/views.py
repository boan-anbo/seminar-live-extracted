from django_filters import rest_framework as filters
# Create your views here.
from rest_framework import viewsets

from djangoProject.speaker.filters import SpeakerFilter
from djangoProject.speaker.models import Speaker
from djangoProject.speaker.serializers import SpeakerSerializer


class SpeakerViewSet(viewsets.ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class=SpeakerFilter
