import datetime

from django.contrib import admin
from django.contrib.admin import TabularInline
from django.utils.translation import ugettext_lazy as _, ugettext_lazy

# Register your models here.
from django.contrib.admin.widgets import FilteredSelectMultiple
from django_admin_relation_links import AdminChangeLinksMixin
from rangefilter.filter import DateRangeFilter

from djangoProject.host.models import Host
from djangoProject.organization.models import Organization
from djangoProject.sources.admin_actions import load
from djangoProject.sources.models import Source
from django import forms

from djangoProject.tag.models import Tag
from djangoProject.webinar.models import Webinar

class WebinarsInline(TabularInline):
    model = Webinar
    show_change_link = True
    fields = ['title', 'startDateTime']
    # filter_horizontal =

class SourceAdminForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Tags'),
            is_stacked=False
        )
    )

    webinars = forms.ModelMultipleChoiceField(
        queryset=Webinar.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Webinars'),
            is_stacked=False
        )
    )

    class Meta:
        model = Source
        exclude = []


    def __init__(self, *args, **kwargs):
        super(SourceAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['tags'].initial = self.instance.tags.all()
            self.fields['webinars'].initial = self.instance.webinars.all()


    def save(self, commit=True):
        Source = super(SourceAdminForm, self).save(commit=False)

        if commit:
            Source.save()

        if Source.pk:
            Source.tags.set(self.cleaned_data['tags'])
            Source.webinars.set(self.cleaned_data['webinars'])

            self.save_m2m()

        return Source

class SourceAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    list_per_page = 25
    form = SourceAdminForm

    change_links = ['webinars', 'tags']
    changelist_links = ['webinars', 'tags']

    # filter_verticle = ['webinars']
    list_display_links = ['id']

    list_display = [
        'created',
        'lastChecked',
        'id',
        'name',
        'sourceType',
        'host_or_org',
        'slugName',
        'url',
        'platformId',
        'organizationId',
        'hostId'
    ]

    search_fields = ['name', 'slugName', 'url', 'host_or_org']

    list_filter = [
        'sourceType',
        ['lastChecked', DateRangeFilter],
        ['created', DateRangeFilter]
    ]

    def get_rangefilter_lastChecked_default(self, request):
        return [datetime.date.today, datetime.datetime.now() + datetime.timedelta(days=7)]

    def get_rangefilter_created_default(self, request):
        return [datetime.date.today, datetime.datetime.now() + datetime.timedelta(days=7)]

    ordering = ['sourceType', 'organizationId', 'slugName']

    list_editable = ['name', 'sourceType', 'platformId','url', 'slugName', 'organizationId', 'hostId']

    readonly_fields = ['id']

    fields = ['id', 'sourceType', 'platformId', 'url', 'slugName', 'organizationId', 'hostId', 'webinars', 'tags']

    inlines = [
        WebinarsInline
    ]
    actions = [
        load,
    ]

    def host_or_org(self, obj: Source):
        if obj.hostId:
            host = Host.objects.get(id=obj.hostId)
            if host:
                return host.__str__()
        if obj.organizationId:
            org = Organization.objects.get(id=obj.organizationId)
            if org:
                return org.__str__()
        return 'None'
    host_or_org.short_description = "Organization or Source"

admin.site.register(Source, SourceAdmin)
