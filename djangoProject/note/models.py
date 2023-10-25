import uuid

from ckeditor.fields import RichTextField
from django.db import models
# Create your models here.
from django.db.models import BooleanField, IntegerField
from django_extensions.db.models import ActivatorModel, TimeStampedModel

from djangoProject.userprofile.models import UserProfile
from djangoProject.webinar.models import Webinar


class Note(TimeStampedModel, ActivatorModel, models.Model):

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = RichTextField(blank=False, default='', max_length=20000)
    isAnonymous=BooleanField(default=False)
    helpfulness = IntegerField(default=0)
    webinar = models.ForeignKey(
        Webinar,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="notes"
    )
    author=models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="notes"
    )

    def __str__(self):
        return self.content[0:25]