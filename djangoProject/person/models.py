import uuid

from django.db import models
# Create your models here.
from django.db.models import ManyToManyField

from djangoProject.webinar.models import Webinar


# class PersonType(models.TextChoices):
#     LANGUAGE = 'LANGUAGE', 'Language'
#     SUBJECT = 'SUBJECT', 'Subject'


class Person(models.Model):

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstName=models.CharField(max_length=100, blank=True)
    firstNameCn=models.CharField(max_length=100, blank=True)
    lastName=models.CharField(max_length=100, blank=True)
    lastNameCn = models.CharField(max_length=100, blank=True)
    # tagType=models.CharField(max_length=255, default=TagType.SUBJECT, choices=TagType.choices)
    organizer_webinars = ManyToManyField(Webinar, blank=True, related_name='organizers')
    note = models.CharField(max_length=255, blank=True)


    slugName=models.CharField(max_length=255, default='', blank=True)

    # speaker_webinars = ManyToManyField(Webinar, blank=True, related_name='speakers')


    def __str__(self):
        if self.firstName is not None and self.lastName is not None:
            return f"{self.firstName} {self.lastName}"
        if self.firstNameCn is not None and self.lastNameCn is not None:
            return f"{self.firstNameCn} {self.lastNameCn}"

