# Create your models here.
import uuid

from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django_extensions.db.models import TimeStampedModel

from djangoProject.userprofile.models import UserProfile
from djangoProject.webinar.models import Webinar


class TaggingRecord(TimeStampedModel, models.Model):

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    userprofile = models.ForeignKey(
        UserProfile,
        null=True,
        on_delete=models.SET_NULL,
        related_name="taggingRecords")



    webinar = models.ForeignKey(
        Webinar,
        on_delete=models.CASCADE,
        related_name="taggingRecords")


    def __str__(self):
        return self.webinar.__str__()

