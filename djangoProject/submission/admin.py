from django.contrib import admin
from django_admin_relation_links import AdminChangeLinksMixin

from djangoProject.lead.models import Lead
from djangoProject.submission.models import Submission

class LeadInline(admin.StackedInline):
    model = Lead
    show_change_link = True


class SubmissionAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    change_links = ['lead']

    changelist_links = ['lead']

    list_display_links = ['id']

    ordering = ['-created']

    list_display = ['id', 'status', 'url', 'description', 'contributor', 'lead' ,'created']

    search_fields = ['description']

    list_editable = ['status']

    readonly_fields = ['id']

    inlines = [LeadInline]

admin.site.register(Submission, SubmissionAdmin)
