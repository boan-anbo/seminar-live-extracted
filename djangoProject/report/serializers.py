from rest_framework import serializers

from djangoProject.report.models import Report


class ReportSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Report
        fields = [
            'id',
            'type',
            'targetId',
            'targetType',
            'content',
            'userprofile'
        ]