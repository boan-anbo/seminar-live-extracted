import uuid

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.db.models import JSONField
from django.template.defaultfilters import truncatechars
from django_extensions.db.models import ActivatorModel, TimeStampedModel
from storages.backends.s3boto3 import S3Boto3Storage
from timezone_field import TimeZoneField

from djangoProject.lead.const import LEAD_SOURCES_ENUM, LeadSources
# Create your models here.
from djangoProject.submission.models import Submission



class Source(TimeStampedModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    sourceType = models.CharField(
        max_length=100,
        choices=LeadSources,
        default=LEAD_SOURCES_ENUM.EVENTBRITE,
        blank=True
    )

    lastChecked = models.DateTimeField(blank=True, null=True)

    organizationId = models.UUIDField(blank=True, null=True)

    hostId = models.UUIDField(blank=True, null=True)

    name = models.CharField(max_length=255, default='')

    notes = RichTextField(max_length=2000, blank=True, default='')

    platformId = models.CharField(max_length=255, default='', blank=True)

    url = models.URLField(max_length=2000, default='', blank=True, unique=True)

    slugName = models.CharField(max_length=2000, default='', blank=True)




    def __str__(self):
        return self.name.__str__()

