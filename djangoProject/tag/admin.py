from django.contrib import admin

# admin.site.register(Tag)
from django.contrib.admin import TabularInline

from djangoProject.tag.admin_actions import update_slug
from djangoProject.tag.models import Tag


# Register your models here.
from djangoProject.tagrelation.models import TagRelation

class TagRelationSubjectTagsInline(TabularInline):
    model = TagRelation
    fk_name = 'subjectTag'
    # fields = ['asSubjectTags__']
    readonly_fields = ['tagrelation_name']

    def tagrelation_name(self, instance: TagRelation):
        return instance.__str__()
    tagrelation_name.short_description = 'Relation'
    verbose_name = 'As Subject'
    verbose_name_plural = 'As Subjects'
    show_change_link = True

#
class TagRelationObjectTagsInline(TabularInline):
    model = TagRelation
    fk_name = 'objectTag'
    verbose_name = 'As Object'
    verbose_name_plural = 'As Objects'
    readonly_fields = ['tagrelation_name']

    def tagrelation_name(self, instance: TagRelation):
        return instance.__str__()
    show_change_link = True

class TagAdmin(admin.ModelAdmin):
    list_per_page = 1000
    # filter_horizontal = ['webinars', 'asSubjectTags', 'asObjectTags']
    ordering = ['tagType', 'name']
    search_fields = ['name', 'namePinyin', 'nameCn']
    list_editable = ['tagType', 'name', 'nameCn', 'namePinyin']
    actions = [update_slug]
    list_display = [
        'id', 'name', 'tagType',  'nameCn', 'namePinyin', 'slugName']
    fields = [
        'name', 'tagType', 'nameCn', 'namePinyin', 'slugName'
    ]
    readonly_fields = ['id']
    inlines = [TagRelationSubjectTagsInline, TagRelationObjectTagsInline]

admin.site.register(Tag, TagAdmin)
