from rest_framework import serializers

from djangoProject.tag.models import Tag
from djangoProject.tagrelation.serializers import TagRelationSerializer


class TagSerializer(serializers.HyperlinkedModelSerializer):
    asSubjectTags = TagRelationSerializer(many=True)
    asObjectTags = TagRelationSerializer(many=True)
    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'nameCn',
            'namePinyin',
            'tagType',
            'asSubjectTags',
            'asObjectTags',
            'slugName'
        ]