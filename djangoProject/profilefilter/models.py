import uuid

from django.db import models

# Create your models here.
from djangoProject.userprofile.models import UserProfile


class ProfileFilter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # views = models.IntegerField(default=0)
    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="filters")

    def __str__(self):
        return str(self.id)