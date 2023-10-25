from rest_framework import serializers

from djangoProject.webinar_stat.models import WebinarStat


class WebinarStatSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = WebinarStat
        fields = ['id', 'views']
