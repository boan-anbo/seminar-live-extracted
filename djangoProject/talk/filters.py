from django_filters import rest_framework as filters

from djangoProject.talk.models import Talk


class TalkFilter(filters.FilterSet):

    class Meta:
        model = Talk
        fields = ['title', 'startDateTime']