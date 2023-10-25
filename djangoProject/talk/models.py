import uuid

from django.db import models

from djangoProject.webinar.models import Webinar


class Talk(models.Model):

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title=models.CharField(max_length=300)
    startDateTime=models.DateTimeField(blank=True, null=True)

    webinar = models.ForeignKey(
        Webinar,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="talks")

    description = models.CharField(max_length=25535, blank=True)

    def __str__(self):
        return self.title

