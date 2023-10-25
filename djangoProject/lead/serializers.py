from rest_framework import serializers

from djangoProject.host.serializers import HostSerializer
from djangoProject.lead.models import Lead
from djangoProject.organization.models import Organization
from djangoProject.tag.serializers import TagSerializer
from djangoProject.webinar.serializers import WebinarSerializer

class NestedHostOrganizationsSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Organization
        fields = ('id', 'name')
        readonly_fields = ('name',)



class LeadSerializer(serializers.HyperlinkedModelSerializer):
    webinar = WebinarSerializer(required=False)
    hosts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tags = TagSerializer(many=True, required=False)
    hostOrganizations = serializers.PrimaryKeyRelatedField(many=True, queryset=Organization.objects.all(), write_only=True)

    class Meta:
        model = Lead
        fields = ['id',
                  'url',
                  'eventUrl',
                  'json',
                  'text',
                  'file',
                  'fileOCR',
                  'html',
                  'created',
                  'startDateTimeString',
                  'webinar',
                  'hostOrganizations',
                  'hosts',
                  'tags',
                  'status'
                  ]

    def create(self, validated_data):
        print(validated_data)
        hostOrganization_ids = validated_data.pop('hostOrganizations', None)

        parent: Lead = super(LeadSerializer, self).create(validated_data)
        # create users here
        if hostOrganization_ids:
            for hostOrganization_id in hostOrganization_ids:
                parent.hostOrganizations.add(hostOrganization_id)
            parent.save()
        return parent
