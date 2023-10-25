from rest_framework import serializers

from djangoProject.link.models import Link


class LinkSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Link
        fields = ['id', 'type', 'url', 'note']