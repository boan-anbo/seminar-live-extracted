import uuid

from django.db import models


# Create your models here.


class WebinarStat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    views = models.IntegerField(default=0)

    def __str__(self):
        return str(self.views)