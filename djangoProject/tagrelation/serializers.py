from rest_framework import serializers

from djangoProject.tagrelation.models import TagRelation


class TagRelationSerializer(serializers.HyperlinkedModelSerializer):
    # userprofile = UserProfileSerializer(many=False, required=False)
    # username

    # only id for the tags of the given record
    subjectTag = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    objectTag = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = TagRelation
        fields = ['subjectTag',  'relation', 'objectTag']