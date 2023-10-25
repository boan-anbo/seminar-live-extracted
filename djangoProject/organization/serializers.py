from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from djangoProject.organization.models import Organization


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    timezone = TimeZoneSerializerField()
    class Meta:
        model = Organization
        fields = ['id', 'name', 'nameShort', 'nameCn', 'nameShortCn', 'timezone', 'color', 'slugName', 'urlPatterns']