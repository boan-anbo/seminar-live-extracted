from django.db import models


class RECOMMEND_LEVEL(models.IntegerChoices):
    NORMAL = 0, '0'
    ONE = 1, '1'
    TWO = 2, '2'
    THREE = 3, '3'

class LANGUAGE(models.TextChoices):
    CHINESE = 'CHINESE', 'Chinese'
    ENGLISH = 'ENGLISH', 'English'

class FILTER_TYPE_ENUM:
    HOST_ORGANIZATION = 'hostOrganizations'
    HOST_PARENT_ORGANIZATION = 'hosts__organizations'
    TAG = 'tags'
    HOST = 'hosts'
    SPEAKER_PERSON = 'talks__speakers__person'

class WEBINAR_TYPES(models.TextChoices):
    WEBINAR = 'WEBINAR', "Webinars"
    CFP = 'CFP', 'Call for participation'
    READING_GROUP = 'READING_GROUP', 'Reading groups'
