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




class Lead(TimeStampedModel, ActivatorModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(max_length=1000, blank=True, default='', unique=True, null=True)
    eventUrl = models.URLField(max_length=1000, blank=True, default='', unique=False)
    startDateTimeString = models.CharField(max_length=255, blank=True)
    file = models.FileField(
        storage=S3Boto3Storage(bucket_name='seminarlive-leads', querystring_auth=True), upload_to='leads', blank=True
    )
    fileOCR = RichTextField(max_length=65535, blank=True)
    text = RichTextField(max_length=65535, blank=True)
    json = JSONField(blank=True, max_length=65535, null=True)

    html = RichTextField(max_length=655350, blank=True)

    # description = RichTextField(blank=True, default='')
    originalStartDateTime = models.DateTimeField(blank=True, null=True)
    originalTimeZone = TimeZoneField(default='Europe/London', choices_display='WITH_GMT_OFFSET')

    # required webinar fields
    title = models.CharField(max_length=255, blank=True)

    description = RichTextField(blank=True, default='')

    startDateTime = models.DateTimeField(blank=True, null=True)

    registrationDeadline = models.DateField(blank=True, null=True)  # actual date time object. stored in UTC.

    source = models.CharField(
        max_length=100,
        choices=LeadSources,
        default=LEAD_SOURCES_ENUM.WEB,
        blank=True
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="leads")

    submission = models.OneToOneField(
        Submission,
        # blank=True,
        # primary_key=True, default=uuid.uuid4, editable=False,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        # if this is not set_null, django won't let webinar linked to this lead to be deleted
        related_name='lead'
    )

    def get_preview_link(self):
        return ""

    def __str__(self):
        return self.id.__str__()

    @property
    def htmlSnippet(self):
        return truncatechars(self.html, 100)

    @property
    def textSnippet(self):
        return truncatechars(self.text, 300)

    @property
    def ocrSnippet(self):
        return truncatechars(self.fileOCR, 300)

    @property
    def jsonSnippet(self):
        return truncatechars(self.json, 300)

    @property
    def urlSnippet(self):
        return truncatechars(self.url, 50)
