# Register your models here.
import datetime

from admin_object_actions.admin import ModelAdminObjectActionsMixin
from django import forms
from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _, ugettext_lazy
from django_admin_relation_links import AdminChangeLinksMixin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

from djangoProject.host.models import Host
from djangoProject.link.models import Link
from djangoProject.note.models import Note
from djangoProject.organization.models import Organization
from djangoProject.person.models import Person
from djangoProject.speaker.models import Speaker
from djangoProject.tag.models import Tag
from djangoProject.talk.models import Talk
from djangoProject.webinar.admin_actions import add_50_sample_webinars, populate_selected_webinars_with_short_url, \
    add_500_sample_webinars, copy_first_webinar_hosts, set_webinar_active
from djangoProject.webinar.admin_object_actions import to_titlecase, make_webinar_only_talk
from djangoProject.webinar.models import Webinar


# class PersonInline(nested_admin.NestedStackedInline):
#     model = Person
#     # sortable_field_name = 'speaker_talks'
#
# class TalkPersonRelationInline(nested_admin.NestedStackedInline):
#     model = Person.speaker_talks.through
#     inlines = (PersonInline,)

class TalkInline(TabularInline):
    model = Talk

    show_change_link = True
    # inlines = [TalkPersonRelationInline]


class NoteInline(TabularInline):
    model = Note
    show_change_link = True
    readonly_fields = ['content']


# class TopLevelAdmin(NestedModelAdmin):
#     model = TopLevel
#     inlines = [LevelOneInline]


class LinkInline(TabularInline):
    model = Link
    show_change_link = True


class HostOrganizationInline(TabularInline):
    model = Organization.hostedWebinars.through
    show_change_link = True
    verbose_name = 'HostOrganizations'
    verbose_name_plural = "HostOrganizations"


class HostInline(TabularInline):
    model = Host.host_webinars.through
    show_change_link = True
    verbose_name = "Hosts"
    verbose_name_plural = "Hosts"


class OrganizersInline(TabularInline):
    model = Person.organizer_webinars.through
    show_change_link = True
    verbose_name = "Organizers"
    verbose_name_plural = "Organizers"


class ParticipantsInline(TabularInline):
    model = Speaker.participant_webinars.through

    show_change_link = True
    verbose_name = "Participant"
    verbose_name_plural = "Participants"


class WebinarAdminForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Tags'),
            is_stacked=False
        )
    )

    hostOrganizations = forms.ModelMultipleChoiceField(
        queryset=Organization.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('HostOrganizations'),
            is_stacked=False
        )
    )

    hosts = forms.ModelMultipleChoiceField(
        queryset=Host.objects.prefetch_related('organizations').all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Hosts'),
            is_stacked=False
        )
    )

    organizers = forms.ModelMultipleChoiceField(
        queryset=Person.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=ugettext_lazy('Organizers'),
            is_stacked=False
        )
    )

    participants = forms.ModelMultipleChoiceField(
        queryset=Speaker.objects.prefetch_related('person', 'talk').all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=ugettext_lazy('Participants'),
            is_stacked=False,

        )
    )

    talks = forms.ModelMultipleChoiceField(
        queryset=Talk.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=ugettext_lazy('Talks'),
            is_stacked=False
        )
    )

    class Meta:
        model = Webinar
        exclude = []

    def __init__(self, *args, **kwargs):
        super(WebinarAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['hostOrganizations'].initial = self.instance.hostOrganizations.all()
            self.fields['hosts'].initial = self.instance.hosts.all()
            self.fields['tags'].initial = self.instance.tags.all()
            self.fields['organizers'].initial = self.instance.organizers.all()
            self.fields['participants'].initial = self.instance.participants.all()
            self.fields['talks'].initial = self.instance.talks.all()

    def save(self, commit=True):
        Webinar = super(WebinarAdminForm, self).save(commit=False)

        if commit:
            Webinar.save()

        if Webinar.pk:
            # Webinar.tags = self.cleaned_data['tags']
            Webinar.hostOrganizations.set(self.cleaned_data['hostOrganizations'])
            Webinar.hosts.set(self.cleaned_data['hosts'])
            Webinar.tags.set(self.cleaned_data['tags'])
            Webinar.organizers.set(self.cleaned_data['organizers'])
            Webinar.participants.set(self.cleaned_data['participants'])
            Webinar.talks.set(self.cleaned_data['talks'])

            self.save_m2m()

        return Webinar


class WebinarAdmin(AdminChangeLinksMixin, ModelAdminObjectActionsMixin, admin.ModelAdmin):
    change_links = ['source', 'hosts', 'lead', 'talks', 'notes', 'organizers', 'participants']
    changelist_links = ['talks', 'notes']
    ordering = ['-created']
    list_per_page = 25
    list_display = [
        'created',
        'status',
        'startDateTimeUTC',
        'startDateTimeZoneLocal',
        'startDateTimeLocal',
        'title',
        'tags_display',
        'hosts_display',
        'description',
        'recommend',
        'id',
        'duration',
        'shortUrl',
        'type',
        # 'talks'
    ]
    list_editable = ['status', 'startDateTimeZoneLocal', 'startDateTimeLocal', 'recommend']
    list_filter = [
        ['startDateTimeUTC', DateRangeFilter],
        ['created', DateRangeFilter],
        'recommended',
        'status',
        'hosts',
        'tags',
    ]

    def get_queryset(self, request):
        qs = super(WebinarAdmin, self).get_queryset(request)
        qs = qs.prefetch_related(
            # 'hosts',
            'tags',
            'hostOrganizations',
            'stat',
            'lead',
            # 'participants',
            # 'organizers',
            'links',
            'notes',
            # 'talks',
            'creator',
            # 'savedBy',
            'source',
        )
        return qs

    def get_rangefilter_startDateTime_default(self, request):
        return [datetime.date.today, datetime.datetime.now() + datetime.timedelta(days=7)]

    def get_rangefilter_created_default(self, request):
        return [datetime.date.today, datetime.datetime.now() + datetime.timedelta(days=7)]

    readonly_fields = ['id', 'shortUrl', 'display_object_actions_detail']
    search_fields = ['title', 'description']
    actions = [
        add_50_sample_webinars,
        add_500_sample_webinars,
        populate_selected_webinars_with_short_url,
        # disabled to prevent accidents in production.
        # remove_all_webinars,
        copy_first_webinar_hosts,
        set_webinar_active
    ]

    object_actions = [
        {
            'slug': 'to_title_case',
            'function': 'to_title_case',
            'verbose_name_past': _('Convert title to title case.'),
        },
        {
            'slug': 'make webinar the only talk',
            'function': 'make_webinar_the_only_talk',
            'verbose_name_past': _('Make webinar the only talk.'),
        },

    ]

    def hosts_display(self, obj: Webinar):
        return ", ".join([
            child.name for child in obj.hosts.all()
        ])

    hosts_display.short_description = "Hosts"

    def tags_display(self, obj: Webinar):
        return ", ".join([
            child.name for child in obj.tags.all()
        ])

    tags_display.short_description = "Tags"

    def to_title_case(self, obj, form):
        to_titlecase(obj)

    def make_webinar_the_only_talk(self, obj, form):
        make_webinar_only_talk(obj)

    # form = WebinarAdminForm

    inlines = [
        # HostInline,
        # LinkInline,
        # OrganizersInline,
        # ParticipantsInline,
        # TalkInline,
        # NoteInline,
        # HostOrganizationInline
    ]

    exclude = [
        'organizers',
        'talks',
        'participants',
        'hosts',
        'extra',
        'savedBy'
    ]


admin.site.register(Webinar, WebinarAdmin)
