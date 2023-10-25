from django.contrib import admin

# admin.site.register(Tag)
from djangoProject.link.models import Link

# Register your models here.


# class LinkAdmin(ModelAdminObjectActionsMixin, admin.ModelAdmin):
#     inlines=[WebinarInline]

admin.site.register(Link)
