from rest_framework import serializers

from djangoProject.tag.serializers import TagSerializer
from djangoProject.taggingrecord.models import TaggingRecord
from djangoProject.userprofile.serializers import UserProfileSerializer


class TaggingRecordSerializer(serializers.HyperlinkedModelSerializer):
    # userprofile = UserProfileSerializer(many=False, required=False)
    # username
    username = serializers.CharField(source='userprofile.user.username', read_only=True)

    # only id for the tags of the given record
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = TaggingRecord
        fields = ['id', 'created', 'tags', 'username']