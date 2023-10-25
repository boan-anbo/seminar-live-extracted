from rest_framework import serializers

from djangoProject.note.serializers import NoteSerializer
from djangoProject.profilefilter.serializers import ProfileFilterSerializer
from djangoProject.submission.serializers import SubmissionSerializer
from djangoProject.user.serializers import UserSerializer
from djangoProject.userprofile.models import UserProfile
from djangoProject.webinar.serializers import WebinarSerializer


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    # submission = SubmissionSerializer(many=True, required=False)
    # notes = NoteSerializer(many=True, required=False)
    user = UserSerializer(many=False, required=False, read_only=True)
    filters = ProfileFilterSerializer(many=True, required=False)
    # savedWebinars = serializers.PrimaryKeyRelatedField(many=True, read_only=True, required=False)
    savedWebinars = WebinarSerializer(many=True, read_only=True, required=False)
    #
    # extra_kwargs = {
    #     'user': {'read_only': True}
    # }

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'savedWebinars',
            'currentView',
            'timezone',
            'language',
            'karma',
            'displayName',
            'filters',
            'isTagger',
            'isRecommender',
            'isDirectPoster',
            'isLeadCollector'
        ]