from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from djangoProject.host.serializers import HostSerializer
from djangoProject.link.serializers import LinkSerializer
from djangoProject.note.serializers import NoteSerializer
from djangoProject.organization.serializers import OrganizationSerializer
from djangoProject.person.serializers import PersonSerializer
from djangoProject.speaker.serializers import SpeakerSerializer
from djangoProject.tag.serializers import TagSerializer
from djangoProject.talk.serializers import TalkSerializer
from djangoProject.webinar.models import Webinar
from djangoProject.webinar_stat.serializers import WebinarStatSerializer


class WebinarSerializer(serializers.HyperlinkedModelSerializer):
    startDateTimeZoneLocal = TimeZoneSerializerField()
    startDateTimeUTC = serializers.DateTimeField()
    # stat = WebinarStatSerializer(required=False)

    extra_kwargs = {
        'extra': {'write_only': True}
    }

    # lead = LeadSerializer(required=False)
    # hosts = HostSerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)
    talks = TalkSerializer(many=True, required=False)
    notes = NoteSerializer(many=True, required=False)
    links = LinkSerializer(many=True, required=False)
    # organizers = PersonSerializer(many=True, required=False)
    participants = SpeakerSerializer(many=True, required=False)
    hostOrganizations = OrganizationSerializer(many=True, required=False)
    lead = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Webinar
        fields = [
            'id',
            'shortUrl',
            'title',
            'tags',
            'language',
            'startDateTimeUTC',
            'startDateTimeLocal',
            'originalUrl',
            'tagCount',
            'type',
            'startDateTimeZoneLocal',
            'poster',
            'lead',
            # 'stat',
            'description',
            # 'hosts',
            # 'organizers',
            'participants',
            'hostOrganizations',
            'notes',
            'extra',
            'talks',
            'links',
            'requiresRegistration',
            'registrationDeadline',
            'hasRecordingOrTranscript',
            'requirement',
            'duration',
            'recommend',
            'status',
            'recommended'
            ]
