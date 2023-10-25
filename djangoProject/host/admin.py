from django.contrib import admin
# Register your models here.
from django.contrib.admin import TabularInline

from djangoProject.host.models import Host
from djangoProject.organization.models import Organization


class OrganizationInline(TabularInline):
    model = Organization.organization_hosts.through
    show_change_link = True

    verbose_name = "Organization"

    verbose_name_plural = "Organizations"



class HostAdmin(admin.ModelAdmin):

    filter_horizontal = ['host_webinars']
    ordering = ['name']
    search_fields = ['name', 'nameCn']
    fields = ['id', 'name', 'nameShort', 'nameCn', 'nameShortCn', 'timezone', 'slugName', 'host_webinars']
    inlines = [OrganizationInline]
    readonly_fields = ['id']


admin.site.register(Host, HostAdmin)
