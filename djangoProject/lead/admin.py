from admin_object_actions.admin import ModelAdminObjectActionsMixin
from django.contrib import admin
# Register your models here.
from django.db import models
from django.db.models import JSONField
from django.forms import CheckboxSelectMultiple
from django.utils.translation import ugettext_lazy as _
# from django.contrib.postgres import fields
# admin.site.register(Tag)
from django_admin_relation_links import AdminChangeLinksMixin
from django_json_widget.widgets import JSONEditorWidget

from djangoProject.host.models import Host
from djangoProject.lead.admin_actions import ocr_eng, ocr_chn, crawl, fetch_file_from_url, sync_to_webinar, set_hnet, \
    set_eventbrite
from djangoProject.lead.admin_object_actions import crawl_one_lead_and_save_json, sync_lead_with_webinar_and_save, \
    convert_local_to_utc_start_datetime
from djangoProject.lead.models import Lead
from djangoProject.organization.models import Organization
from djangoProject.tag.models import Tag
from djangoProject.webinar.models import Webinar


class WebinarInline(admin.StackedInline):
    model = Webinar
    show_change_link = True

class TagInLine(admin.StackedInline):
    model = Tag.leads.through
    show_change_link = True

class HostInLine(admin.StackedInline):
    model = Host.host_leads.through
    show_change_link = True

class HostOrganizationInline(admin.StackedInline):
    model = Organization.hostedLeads.through
    show_change_link = True



class LeadAdmin(AdminChangeLinksMixin, ModelAdminObjectActionsMixin, admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    changelist_links = ['webinar', 'urlSnippet']
    filter_horizontal = ['hostOrganizations']

    change_links = ['webinar', 'hostOrganizations'] # from django_admin_relation_links package. used to show a change link to a related model, the webinar of the lead in my case. this is not used because I'm using the native show_change_link option and only using the 3rd party change list option
    list_display = [
        # 'display_object_actions_list', # for object actions
        'created',
        'status',
        'startDateTimeString',
        'webinar_link',
        'source',
        'urlSnippet',
        'hostOrganizations_display',
        'jsonSnippet',
        'textSnippet',
        'file',
        'ocrSnippet',
        'htmlSnippet',
        'id',
        'hosts',
        'tags',
        'hostOrganizations',

    ]
    # get names of the array of host organizations on list view of Lead.
    def hostOrganizations_display(self, obj: Lead):
        return ", ".join([
            child.__str__() for child in obj.hostOrganizations.all()
        ])

    hostOrganizations_display.short_description = "Host Organizations"

    list_filter = ['status', 'created', 'source']
    list_display_links = ['created','urlSnippet']
    list_editable = ['status', 'source']
    search_fields = ['html', 'hostOrganizations__name', 'url']
    autocomplete_fields = ['hostOrganizations']

    # fields = ['display_object_actions_detail']
    readonly_fields = ['display_object_actions_detail']

    actions_selection_counter = True
    ordering = ['-created']
    change_form_template = "lead_change_form.html"
    inlines = [WebinarInline, TagInLine, HostInLine, HostOrganizationInline]
    exclude= ['deactivate_date']

    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }

    # actions for LIST view
    actions = [
        ocr_eng,
        ocr_chn,
        fetch_file_from_url,
        crawl,
        sync_to_webinar,
        set_hnet,
        set_eventbrite,
    ]

    # actions for Object view
    object_actions = [
        {
            'slug': 'preview',
            'function': 'preview',
            'verbose_name': _('preview json'),
            'verbose_name_past': _('preview has shown'),
        },
        {
            'slug': 'crawl',
            'function': 'crawl',
            'verbose_name': _('crawl the entity '),
            'verbose_name_past': _('crawl finished and saved to json'),
        },
        {
            'slug': 'sync webinar',
            'function': 'sync',
            'verbose_name_past': _('synced with webinar and saved to json'),
        },
        {
            'slug': 'local to utc startDateTime',
            'function': 'local_to_utc',
            'verbose': _('local to utc start datetime')
        }
    ]

    def preview(self, obj, form):
        print(obj)

    def crawl(self, obj: Lead, form):
        crawl_one_lead_and_save_json(obj)

    def sync(self, obj: Lead, form):
        sync_lead_with_webinar_and_save(obj)

    def local_to_utc(self, obj: Lead, form):
        convert_local_to_utc_start_datetime(obj)


admin.site.register(Lead, LeadAdmin)
