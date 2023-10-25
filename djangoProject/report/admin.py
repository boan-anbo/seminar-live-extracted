from django.contrib import admin

# class LinkAdmin(ModelAdminObjectActionsMixin, admin.ModelAdmin):
#     inlines=[WebinarInline]
from djangoProject.report.models import Report

# admin.site.register(Tag)
# Register your models here.

admin.site.register(Report)
