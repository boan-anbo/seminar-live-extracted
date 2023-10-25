import uuid

from django.db import models
# Create your models here.
from django.db.models import ManyToManyField

from djangoProject.lead.models import Lead
from djangoProject.sources.models import Source
from djangoProject.taggingrecord.models import TaggingRecord
from djangoProject.webinar.models import Webinar


class TagType(models.TextChoices):
    LANGUAGE = 'LANGUAGE', 'Language' # languages
    DOMAIN = 'DOMAIN', 'Domain' # humanities, sciences,
    DISCIPLINE = 'DISCIPLINE', 'Discipline' # eg. History, Computer Science
    SUBFIELD = 'SUBFIELD', 'Subfield' # eg. media studies. computer graphics
    TOPIC = 'TOPIC', 'Topic', # inequality, prediction accuracy
    AREA = 'AREA', 'Area' # Area


# class TagDiscipline(models.TextChoices):
#     PHILOSOPHY = 'PHILOSOPHY', 'Philosophy'
#     LITERATURE = 'LITERATURE', 'Literature'
#     ART = 'ART', 'Art'
#     POLITICS = 'POLITICS', 'Politics'
#     ECONOMICS = 'ECONOMICS', 'Economics'
#     LAW = 'LAW', 'Law'
#     SOCIOLOGY = 'SOCIOLOGY', 'Sociology'
#     ANTHROPOLOGY = 'ANTHROPOLOGY', 'Anthropology'
#     HISTORY = 'HISTORY', 'History'

# class TagTopic(models.TextChoices):
#     GENERAL = 'GENERAL', 'General'
#     CHINA = 'CHINA', 'China'
#     JAPAN = 'JAPAN', 'Japan'
#     INDIA = 'INDIA', 'India'




class Tag(models.Model):

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=100)
    nameCn = models.CharField(max_length=100, default='')
    slugName=models.CharField(max_length=100, default='', blank=True)
    namePinyin = models.CharField(max_length=100, default='')
    tagType=models.CharField(max_length=255, default=TagType.TOPIC, choices=TagType.choices)
    # tagDiscipline=models.CharField(max_length=255, default=TagDiscipline.PHILOSOPHY, choices=TagDiscipline.choices)
    # TagTopic = models.CharField(max_length=255, default=TagTopic.GENERAL, choices=TagTopic.choices)
    webinars = ManyToManyField(Webinar, blank=True, related_name='tags')
    taggingrecords = ManyToManyField(TaggingRecord, blank=True, related_name='tags')


    leads = ManyToManyField(Lead, blank=True, related_name='tags')
    sources = ManyToManyField(Source, blank=True, related_name='tags')

    def __str__(self):
        return "(" + self.tagType + ") " +self.name

