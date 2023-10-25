# Create your models here.

import uuid

from django.db import models
from django.db.models import ManyToManyField

from djangoProject.person.models import Person
from djangoProject.talk.models import Talk
from djangoProject.webinar.models import Webinar


class Speaker(models.Model):

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person=models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, null=True, related_name='speakers')
    talk=models.ForeignKey(Talk, on_delete=models.CASCADE, blank=True, null=True, related_name='speakers')
    affiliation = models.CharField(max_length=2000, blank=True)

    participant_webinars = ManyToManyField(Webinar, blank=True, related_name='participants')


    def __str__(self):
        if self.affiliation and len(self.affiliation) > 0:
            return  self.person.__str__() + " (" + self.affiliation + ")"
        else:
            return self.person.__str__()

