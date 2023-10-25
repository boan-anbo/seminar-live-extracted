# Create your views here.
from django_filters import rest_framework as filters
from rest_framework import viewsets

from djangoProject.person.filters import PersonFilter
from djangoProject.person.models import Person
from djangoProject.person.serializers import PersonSerializer



class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all().order_by('lastName')
    serializer_class = PersonSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class=PersonFilter
