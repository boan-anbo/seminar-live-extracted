from rest_framework import serializers

from djangoProject.person.serializers import PersonSerializer
from djangoProject.speaker.models import Speaker


class SpeakerSerializer(serializers.HyperlinkedModelSerializer):
    person = PersonSerializer(many=False, required=False)
    class Meta:
        model = Speaker
        fields = ['id', 'person', 'affiliation']




    def __str__(self):
        return self.person.__str__()