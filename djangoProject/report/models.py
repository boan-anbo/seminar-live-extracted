# Create your models here.

import uuid

from django.db import models

from djangoProject.person.models import Person
from djangoProject.talk.models import Talk
from djangoProject.userprofile.models import UserProfile
from djangoProject.webinar.models import Webinar


class ReportTargetType(models.TextChoices):
    WEBINAR = 'WEBINAR', 'Webinar'
    LINK = 'LINK', 'Link'

class ReportType(models.TextChoices):
    INCORRECT_INFO = 'INCORRECT_INFO', "Incorrect Information"
    SUGGESTION = 'SUGGESTION', 'Suggestion'
    BUG = 'BUG', 'Bug'
    ADD_INFO = 'ADD_INFO', 'Add new information'
    DELETE_REQUEST = 'DELETE_REQUEST', "Request deletion of an item"

class Report(models.Model):

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    targetId=models.CharField(max_length=255, blank=True, null=True)
    targetType=models.CharField(max_length=255, choices=ReportTargetType.choices, blank=True, null=True)
    type=models.CharField(max_length=255, choices=ReportType.choices)
    content=models.CharField(max_length=3000, blank=False)
    userprofile=models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reports"
    )


    def __str__(self):
        return self.__str__()

