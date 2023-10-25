from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from djangoProject.host.models import Host
from djangoProject.organization.serializers import OrganizationSerializer


class HostSerializer(serializers.HyperlinkedModelSerializer):
    organizations = OrganizationSerializer(many=True, required=False)
    timezone = TimeZoneSerializerField()

    class Meta:
        model = Host
        fields = [
            'id',
            'name',
            'nameShort',
            'nameCn',
            'nameShortCn',
            'slugName',
            'organizations',
            'timezone'
        ]