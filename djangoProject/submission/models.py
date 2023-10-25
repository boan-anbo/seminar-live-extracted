import uuid

from ckeditor.fields import RichTextField
from django.db import models
# Create your models here.
from django.db.models import URLField
from django_extensions.db.models import ActivatorModel, TimeStampedModel

from djangoProject.userprofile.models import UserProfile


class Submission(TimeStampedModel, ActivatorModel, models.Model):

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = URLField(blank=True, default='', max_length=2000)
    description = RichTextField(blank=True, default='')
    contributor=models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="submissions"
    )

    def __str__(self):
        return self.id.__str__()