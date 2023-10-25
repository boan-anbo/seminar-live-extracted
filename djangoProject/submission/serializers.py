from rest_framework import serializers

# Register your models here.
from djangoProject.submission.models import Submission


class SubmissionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Submission
        fields = ['id', 'url', 'description', 'created', 'modified', 'lead', 'status']


    # class UserSerializer(serializers.ModelSerializer):
    #
    #     class Meta:
    #         model = User
    #
    #     def get_days_since_joined(self, obj):
    #         return (now() - obj.date_joined).days