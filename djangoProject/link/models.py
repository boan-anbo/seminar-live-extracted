import uuid

from django.db import models

from djangoProject.link.const import LinkTypes
from djangoProject.webinar.models import Webinar


# Create your models here.


class Link(models.Model):

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    type = models.CharField(
        max_length=100,
        choices=LinkTypes,
    )

    note = models.CharField(
        max_length=280,
        default='',
        blank=True
    )

    url = models.CharField(
        max_length=1000,
        blank=False
    )

    webinar = models.ForeignKey(
        Webinar,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="links")

    def __str__(self):
        return self.type + ': ' + self.url

