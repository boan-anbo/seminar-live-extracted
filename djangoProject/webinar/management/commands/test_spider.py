import json
import re
from typing import cast, List

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from scrapy.utils.serialize import ScrapyJSONEncoder

from djangoProject.sources.actions import get_future_events_by_slugname, save_webinar_from_eventbrite_view_event
from scraping_center.apis.eventbrite import fetch_eventbrite_one_by_id
from scraping_center.scrapy_project.run_scrape_spiders import startSpider
from scraping_center.scrapy_project.scrapy_project.models.event_view_item import EventViewItem
from scraping_center.scrapy_project.scrapy_project.spiders.eventbrite_list import EventbriteListSpider




class Command(BaseCommand):
    help = 'Test event'

    def handle(self, *args, **options):
        events = get_future_events_by_slugname('brown-university-8695100606')
        for e in events:
            webinar = save_webinar_from_eventbrite_view_event(e)
            webinar.save()

