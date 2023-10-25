from typing import cast

from django.contrib.admin import ModelAdmin
from django.db.models import QuerySet

from djangoProject.link.const import LINK_TYPE_ENUM
from djangoProject.link.models import Link
from djangoProject.util_functions.populate_short_url import populate_short_url
from djangoProject.webinar.functions import generate_webinar
from djangoProject.webinar.models import Webinar

def set_webinar_active(modeladmin: ModelAdmin, request, queryset: QuerySet):
    for index, webinar in enumerate(queryset):
        webinar.status = True
        webinar.save()

        # print(item.hosts[0])
set_webinar_active.short_description = "Set Selected Webinars Active"

def copy_first_webinar_hosts(modeladmin: ModelAdmin, request, queryset: QuerySet):
    first_webinar = queryset.first()
    for index, webinar in enumerate(queryset):
        if webinar.id != first_webinar.id:
            webinar.hosts.set(first_webinar.hosts.all())
            webinar.save()

        # print(item.hosts[0])
copy_first_webinar_hosts.short_description = "Copy First Webinar's Hosts"

def add_50_sample_webinars(modeladmin: ModelAdmin, request, queryset: QuerySet):
    for x in range(0, 50):
        new_webinar = generate_webinar(x)
        new_webinar.save()
add_50_sample_webinars.short_description = 'add 50 sample webianrs'

def add_500_sample_webinars(modeladmin: ModelAdmin, request, queryset: QuerySet):
    for x in range(0, 500):
        new_webinar = generate_webinar(x)
        new_webinar.save()
add_500_sample_webinars.short_description = 'add 500 sample webianrs'

#Delete all webinars in admin
def remove_all_webinars(modeladmin: ModelAdmin, request, queryset: QuerySet):
    Webinar.objects.all().delete()


def populate_selected_webinars_with_short_url(modeladmin: ModelAdmin, request, queryset: QuerySet):
    for item in queryset:
        webinar = cast(Webinar, item)
        webinar = populate_short_url(webinar)
        webinar.save()


        link1 = Link()
        link1.url = 'http://www.zoom.com'
        link1.type = LINK_TYPE_ENUM.EVENT
        link1.note = "this is the main link"
        link1.webinar = webinar
        link1.save()
        link2 = Link()
        link2.url = 'http://www.tencent.com'
        link2.type = LINK_TYPE_ENUM.REGISTRATION
        link2.note = "This is the Tencent webinar link:"
        link2.webinar = webinar
        link2.save()

        # webinar.organizers.add(Person.objects.get(firstName='Leonel'))
        # webinar.organizers.add(Person.objects.get(firstName='Christiano'))
        webinar.save()
populate_selected_webinars_with_short_url.short_description = "Fill with short url"


