from django.contrib import admin

# Register your models here.
from djangoProject.organization.models import Organization


class OrganizationAdmin(admin.ModelAdmin):

    ordering = ['name']
    search_fields = ['name']
    readonly_fields = ['id']
    list_editable = ['urlPatterns', 'color']
    list_display = ['id', 'name', 'nameShort', 'color', 'urlPatterns']
    fields = [
        'id',
        'name',
          'nameShort',
          'nameCn',
          'nameShortCn',
          'color',
          'slugName',
          'timezone',
          # 'organization_hosts',
          'hostedWebinars',
          'hostedLeads',
        'urlPatterns'
              ]


admin.site.register(Organization, OrganizationAdmin)
