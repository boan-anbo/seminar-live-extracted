import uuid

from ckeditor.fields import RichTextField
from django.db import models
# Create your models here.
# from django.utils import timezone
from django.db.models import ManyToManyField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel, ActivatorModel
from timezone_field import TimeZoneField

from djangoProject.lead.models import Lead
from djangoProject.sources.models import Source
from djangoProject.userprofile.models import UserProfile
from djangoProject.webinar.const import RECOMMEND_LEVEL, LANGUAGE, WEBINAR_TYPES
from djangoProject.webinar_stat.models import WebinarStat


class Webinar(TimeStampedModel, ActivatorModel, models.Model):
    # auto fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isVisible = models.BooleanField(default=False)

    # required fields
    title = models.CharField(max_length=255)
    startDateTimeLocal = models.DateTimeField(blank=True, null=True, verbose_name='Original Start DateTime (local)')
    startDateTimeUTC = models.DateTimeField(verbose_name='Start DateTime (UTC)') # actual date time object. stored in UTC.

    # optional fields
    startDateTimeZoneLocal = TimeZoneField(max_length=100, verbose_name='Start DateTime (Local)', choices_display='WITH_GMT_OFFSET', null=True, default='UTC') # the local timezone for the event.
    description = RichTextField(blank=True, default='')
    duration = models.IntegerField(default=120, blank=True) # unit: minutes
    shortUrl = models.CharField(max_length=255, blank=True)

    originalUrl = models.URLField(max_length=3000, blank=True)

    savedBy = ManyToManyField(UserProfile, blank=True, related_name='savedWebinars')

    type = models.TextField(default=WEBINAR_TYPES.WEBINAR, choices=WEBINAR_TYPES.choices)

    hasRecordingOrTranscript = models.BooleanField(default=False)

    language = models.TextField(default=LANGUAGE.ENGLISH, choices=LANGUAGE.choices, blank=True)

    recommend = models.IntegerField(default=RECOMMEND_LEVEL.NORMAL, choices=RECOMMEND_LEVEL.choices, blank=True)

    poster = models.FileField(
        upload_to='posters',
        blank=True
    )

    extra = RichTextField(blank=True) # for all unformatted extra data that might be used later.
    stat = models.OneToOneField(
        WebinarStat,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    tagCount = models.IntegerField(default=0, blank=False)  # number of tags applied

    recommended = models.BooleanField(default=False)

    # I was hoping to set this on lead side, however, only by putting it on the webinar side can i use the inline admin
    lead = models.OneToOneField(
        Lead,
        # blank=True,
        # primary_key=True, default=uuid.uuid4, editable=False,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        # if this is not set_null, django won't let webinar linked to this lead to be deleted
        related_name='webinar'
    )

    sourcePlatformId = models.CharField(max_length=255, null=True, blank=True)

    source = models.ForeignKey(
        Source,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="webinars")



    requiresRegistration = models.BooleanField(blank=True, default=True)
    requirement = models.CharField(max_length=280, blank=True, default='')
    registrationDeadline = models.DateField(blank=True, null=True) # actual date time object. stored in UTC.

    creator = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="createdWebinars"
    )

    def __str__(self):
        return self.title

@receiver(post_save, sender=Webinar)
def create_stat(sender, instance, created, **kwargs):
    if created:
        instance.stat=WebinarStat.objects.create()
        instance.save()
