from django.contrib import admin
# Register your models here.
from django.contrib.admin import TabularInline
# admin.site.register(Tag)
from django_admin_relation_links import AdminChangeLinksMixin

from djangoProject.speaker.models import Speaker
from djangoProject.talk.models import Talk


class SpeakerInline(TabularInline):
    model = Speaker
    show_change_link = True
    autocomplete_fields = ['person']

# class WebinarInline(TabularInline):
#     model = Webinar
#     show_change_link = True



class TalkAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    # the change links provided by 'django_admin_relation_links' nicely complements the native django 'show_change_link' option. where show_change_link is good for inline display of the submember of the inlined item, the change_link option is good for display a link to ONE ITEM on the reverse end.
    change_links = ['webinar', 'speakers']
    inlines = [SpeakerInline]


    changelist_links = ['webinar']
    list_display = [
        'title',
        'webinar',
        'speakers_display',
        'startDateTime',
        'description',
        # 'speakers',
    ]
    # readonly_fields = ['id', 'shortUrl', 'display_object_actions_detail']
    search_fields = ('webinar', )

    def speakers_display(self, obj: Talk):
        return ", ".join([
            child.__str__() for child in obj.speakers.all()
        ])
    speakers_display.short_description = "Speakers"


admin.site.register(Talk, TalkAdmin)
