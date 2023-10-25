from django.contrib.admin import ModelAdmin
from django.db.models import QuerySet

from djangoProject.tag.actions import populate_tag_slugname


def update_slug(modeladmin: ModelAdmin, request, queryset: QuerySet):
    for index, tag in enumerate(queryset):
        updated_tag = populate_tag_slugname(tag)

        updated_tag.save()
