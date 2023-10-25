import datetime
import time

from django.contrib.admin import ModelAdmin
from django.db.models import QuerySet

from djangoProject.sources.actions import get_future_events_by_slugname, save_webinar_from_eventbrite_view_event


def load(modeladmin: ModelAdmin, request, queryset: QuerySet):
    for index, source in enumerate(queryset):

        events = get_future_events_by_slugname(source.slugName)
        for e in events:
            time.sleep(3)
            save_webinar_from_eventbrite_view_event(e, source)
            source.lastChecked = datetime.datetime.now()
            source.save()
            # webinar.save()
        print(source.name)
load.short_description = "Load webinars from the source"

