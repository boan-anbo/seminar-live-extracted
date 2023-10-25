from django.db import models


class TagRelationType(models.TextChoices):
    PARENT_TO_CHILD = 'PARENT_TO_CHILD', 'Parent to Child'
    EQUAL = 'EQUAL', 'Equal'