from rest_framework import serializers

from djangoProject.speaker.serializers import SpeakerSerializer
from djangoProject.talk.models import Talk


class TalkSerializer(serializers.HyperlinkedModelSerializer):
    speakers = SpeakerSerializer(many=True, required=False)
    class Meta:
        model = Talk
        fields = ['id', 'title', 'startDateTime', 'speakers']