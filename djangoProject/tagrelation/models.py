import uuid

from django.db import models

# Create your models here.
from django.db.models import ManyToManyField

from djangoProject.tag.models import Tag
from djangoProject.tagrelation.const import TagRelationType


class TagRelation(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    relation = models.CharField(max_length=100, default=TagRelationType.PARENT_TO_CHILD, choices=TagRelationType.choices)

    subjectTag = models.ForeignKey(
        Tag,
        verbose_name='Subject Tag',
        on_delete=models.CASCADE,
        related_name="asSubjectTags")

    objectTag = models.ForeignKey(
        Tag,
        verbose_name='Object Tag',

        on_delete=models.CASCADE,
        related_name="asObjectTags")

    def __str__(self):
        if self.relation == TagRelationType.PARENT_TO_CHILD:
            return self.subjectTag.__str__() + " >>> " + self.objectTag.__str__()
        if self.relation == TagRelationType.EQUAL:
            return self.subjectTag.__str__() + " === " + self.objectTag.__str__()

