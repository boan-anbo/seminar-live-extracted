import uuid

from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.db.models import ManyToManyField
from django_extensions.db.models import TimeStampedModel

from djangoProject.user.const import VIEW_TYPE_ENUM
from djangoProject.userprofile.const import LANGUAGE_TYPE_ENUM


class UserProfile(TimeStampedModel, models.Model):

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    displayName = models.CharField(max_length=30, blank=True)

    currentView=models.CharField(max_length=280, default=VIEW_TYPE_ENUM.TODAY)


    timezone = models.CharField(max_length=100, blank=True, default='Europe/London')

    showSavedOnly = models.BooleanField(default=False)

    karma = models.IntegerField(default=5)

    language = models.CharField(max_length=20, default=LANGUAGE_TYPE_ENUM.EN)

    isTagger = models.BooleanField('Tagger status', default=False)

    isRecommender = models.BooleanField('Recommender status', default=False)

    isDirectPoster = models.BooleanField('Direct Poster', default=False)

    isLeadCollector = models.BooleanField('Lead Poster', default=False)

    def __str__(self):
        return self.user.__str__()

