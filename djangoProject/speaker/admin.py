from django.contrib import admin

from djangoProject.speaker.models import Speaker


class SpeakerAdmin(admin.ModelAdmin):
    autocomplete_fields = ['person', 'participant_webinars']

    list_display = ['id','person', 'affiliation', 'talk']
    list_display_links = ['person', 'id', 'affiliation']


admin.site.register(Speaker, SpeakerAdmin)
