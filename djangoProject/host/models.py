from uuid import uuid4

from colorfield.fields import ColorField
from django.db import models
# Create your models here.
from django.db.models import ManyToManyField
from timezone_field import TimeZoneField

from djangoProject.lead.models import Lead
from djangoProject.organization.models import Organization
from djangoProject.sources.models import Source
from djangoProject.webinar.models import Webinar


class Host(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    timezone = TimeZoneField(default='Europe/London', choices_display='WITH_GMT_OFFSET')

    name = models.CharField(max_length=255)
    nameShort = models.CharField(max_length=50, blank=True)

    nameCn = models.CharField(max_length=255, blank=True)
    nameShortCn = models.CharField(max_length=50, blank=True)




    organizations = ManyToManyField(
        Organization,
        blank=True,
        related_name='organization_hosts'
    )

    slugName=models.CharField(max_length=255, default='', blank=True)

    color = ColorField(blank=True, null=True)

    # fixme For now, only use one host per seminar. the problem is that there is no reliable way to control the output ordering if a webinar has multiple hosts.
    host_webinars = ManyToManyField(Webinar, blank=True, related_name='hosts')

    host_leads = ManyToManyField(Lead, blank=True, related_name='hosts')

    host_sources = ManyToManyField(Source, blank=True, related_name='hosts')
    def __str__(self):
        if self.organizations.first():
            return "(" + self.organizations.first().__str__() + ") " +self.name
        else:
            return self.name

