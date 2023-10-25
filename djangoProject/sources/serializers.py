from rest_framework import serializers

from djangoProject.host.serializers import HostSerializer
from djangoProject.lead.models import Lead
from djangoProject.organization.models import Organization
from djangoProject.sources.models import Source
from djangoProject.tag.serializers import TagSerializer
from djangoProject.webinar.serializers import WebinarSerializer



class SourceSerializer(serializers.HyperlinkedModelSerializer):
    webinars = WebinarSerializer(many=True, required=False)
    hosts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tags = TagSerializer(many=True, required=False)
    hostOrganizations = serializers.PrimaryKeyRelatedField(many=True, queryset=Organization.objects.all(), write_only=True, required=False)

    class Meta:
        model = Source
        fields = ['id',
                  'platformId',
                  'sourceType',
                  'url',
                  'name',
                  'webinars',
                  'organizationId',
                  'hostId',
                  'hostOrganizations',
                  'hosts',
                  'tags',
                  'slugName'

                  ]

