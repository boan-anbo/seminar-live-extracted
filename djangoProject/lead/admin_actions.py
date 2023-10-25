from typing import cast

import requests
from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.core.files import File
from django.db.models import QuerySet

from djangoProject.lead.admin_object_actions import crawl_one_lead_and_save_json, sync_lead_with_webinar_and_save
from djangoProject.lead.const import LEAD_SOURCES_ENUM
from djangoProject.lead.models import Lead
from scraping_center.ocr_functions.ocr_functions import openocr_image


def ocr_with_lang(queryset: QuerySet, lang: str):
    count = 0
    for item in queryset:
        lead = cast(Lead, item)
        ocr_text = openocr_image(lead.file.url, lang)
        if ocr_text is not None and len(ocr_text) > 0:
            lead.fileOCR = ocr_text
            lead.save()
            count += 1


def ocr_eng(modeladmin, request, queryset: QuerySet):
    ocr_with_lang( queryset, 'eng')
ocr_eng.short_description = "OCR English"




def ocr_chn(modeladmin, request, queryset: QuerySet):
    ocr_with_lang( queryset, 'chi_sim')
ocr_chn.short_description = "OCR Chinese"






def crawl(modeladmin, request, queryset: QuerySet):
    for item in queryset:
        lead = cast(Lead, item)
        try:
            crawl_one_lead_and_save_json(lead)
            modeladmin.message_user(request, "Item Crawled and saved to json")
        except:
            raise

crawl.short_description = "crawl by source type"


def fetch_file_from_url(modeladmin, request, queryset: QuerySet):
    for item in queryset:
        lead = cast(Lead, item)
        response = requests.get(lead.url)
        # truncate the file name if too long
        fileName = lead.url.split('/')[-1]
        if len(fileName) > 20:
            fileName = fileName[-20:]
        open(fileName, 'wb').write(response.content)
        local_file = open(fileName, 'rb')
        file = File(local_file)
        # file = File(response.content)
        if response is not None:
            # lead.file = response
            lead.file.save(fileName, file)
        print(lead)

fetch_file_from_url.short_description = 'Fetch From Url'



def sync_to_webinar(modeladmin: ModelAdmin, request, queryset: QuerySet):
    for item in queryset:
        lead = cast(Lead, item)
        # check if webinar already exists


        try:
            sync_lead_with_webinar_and_save(lead)
        except ValueError as e:
            modeladmin.message_user(request, f'Lead Sync Error: {e}', messages.ERROR)
    return
sync_to_webinar.short_description = 'sync with webinar'

def set_hnet(modeladmin, request, queryset: QuerySet):
    for item in queryset:
        lead = cast(Lead, item)
        try:
            lead.source = LEAD_SOURCES_ENUM.HNET
            lead.save()
            modeladmin.message_user(request, "Item source set to Hnet")
        except:
            raise
crawl.short_description = "Set item source to H-net"

def set_eventbrite(modeladmin, request, queryset: QuerySet):
    for item in queryset:
        lead = cast(Lead, item)
        try:
            lead.source = LEAD_SOURCES_ENUM.EVENTBRITE
            lead.save()
            modeladmin.message_user(request, "Item source set to Eventbrite")
        except:
            raise
crawl.short_description = "Set item source to Eventbrite"