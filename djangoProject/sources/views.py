import re
from typing import cast

from django.db.models.signals import post_save
from django.dispatch import receiver

from djangoProject.lead.const import LEAD_SOURCES_ENUM
from djangoProject.sources.models import Source
from djangoProject.sources.serializers import SourceSerializer

# Create your views here.

@receiver(post_save, sender=Source)
def default_lead_status_to_inactive(sender, instance, **kwargs):
    instance = cast(Source, instance)
    if kwargs.get('created', False):
        url = getattr(instance, 'url', None)
        if url and instance.sourceType == LEAD_SOURCES_ENUM.EVENTBRITE:
            slugname = re.findall(r'o\/(.*-[0-9]*)', url)[0]
            if slugname:
                instance.slugName = slugname
                instance.save()

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser



class SourcePostView(CreateAPIView):
    # this empty the project setting for authentications in order to easy the CSRF token authentication for Post, i.e. when you try to post leads.
    # authentication_classes = []

    queryset = Source.objects.all().order_by('created')
    serializer_class = SourceSerializer
    # filter_backends = [filters.DjangoFilterBackend]
    # filterset_class = LeadFilter
    permission_classes = [IsAdminUser]

