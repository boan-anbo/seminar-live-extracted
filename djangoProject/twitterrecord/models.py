import uuid

from django.db import models

# Create your models here.
from django_extensions.db.models import TimeStampedModel

from djangoProject.webinar.models import Webinar


class TwitterRecord(TimeStampedModel, models.Model):

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tweetId=models.CharField(max_length=255, blank=True, null=False)
    webinar = models.ForeignKey(
        Webinar,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="twitterRecords")

    inReplyToTargetId = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.tweetId

