import uuid

from colorfield.fields import ColorField
from django.db import models
# Create your models here.
from django.db.models import ManyToManyField
from timezone_field import TimeZoneField

from djangoProject.lead.models import Lead
from djangoProject.sources.models import Source
from djangoProject.webinar.models import Webinar


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    nameShort = models.CharField(max_length=50, blank=True)
    nameCn = models.CharField(max_length=255, blank=True)
    nameShortCn = models.CharField(max_length=50, blank=True)

    timezone = TimeZoneField(default='Europe/London', choices_display='WITH_GMT_OFFSET')

    hostedWebinars = ManyToManyField(Webinar, blank=True, related_name='hostOrganizations')

    hostedLeads = ManyToManyField(Lead, blank=True, related_name='hostOrganizations')

    hostedSources = ManyToManyField(Source, blank=True, related_name='hostOrganizations')

    color = ColorField(blank=True, null=True)

    slugName=models.CharField(max_length=255, default='', blank=True)

    urlPatterns = models.CharField(max_length=1000, blank=True, default='')

    def __str__(self):
        return self.name

