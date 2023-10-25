from django.contrib import admin
from django_admin_relation_links import AdminChangeLinksMixin

from djangoProject.note.models import Note


class NoteAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    change_links = ['webinar']

    changelist_links = ['webinar']

    list_display_links = ['webinar']

    list_display = ['status', 'content', 'webinar', 'author', 'isAnonymous','created']

    search_fields = ['content']

    list_editable = ['status']

    readonly_fields = ['id']

admin.site.register(Note, NoteAdmin)
