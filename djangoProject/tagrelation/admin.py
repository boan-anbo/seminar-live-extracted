from django.contrib import admin

# Register your models here.
from django.contrib.admin import TabularInline
from django_admin_relation_links import AdminChangeLinksMixin

from djangoProject.tag.models import Tag
from djangoProject.tagrelation.models import TagRelation

# class SubjectTagInline(admin.TabularInline):
#     model = TagRelation.
#
#
# @admin.register(User)
# class MyUserAdmin(UserAdmin):
#     inlines = [CompanyInline, ]
class TagInline(TabularInline):
    model = Tag


class TagRelationAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    # change_links = ['lead']
    #
    # changelist_links = ['lead']
    #
    # list_display_links = ['id']
    #
    # ordering = ['-created']
    inline = [TagInline]
    readonly_fields = ['id']
    # filter_horizontal = ['subjectTags', 'objectTag']
    # list_display = ['id', 'status', 'url', 'description', 'contributor', 'lead' ,'created']

    # search_fields = ['description']


admin.site.register(TagRelation, TagRelationAdmin)