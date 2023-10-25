from rest_framework import serializers

from djangoProject.profilefilter.models import ProfileFilter


class ProfileFilterSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProfileFilter
        fields = ['id']