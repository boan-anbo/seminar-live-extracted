import datetime
import json

import pytz
from scrapy.utils.serialize import ScrapyJSONEncoder

from djangoProject.lead.const import LEAD_SOURCES_ENUM
from djangoProject.lead.lead_adapters.adpters import sync_lead_json_with_webinar
from djangoProject.lead.models import Lead
from djangoProject.link.const import LINK_TYPE_ENUM
from djangoProject.link.models import Link
from djangoProject.util_functions.populate_short_url import populate_short_url
from djangoProject.webinar.models import Webinar
from scraping_center.scrapy_project.run_scrape_spiders import startSpider
from scraping_center.scrapy_project.scrape_methods import eventbrite_events
from scraping_center.scrapy_project.scrapy_project.spiders.hnet import HnetEventSpider


def crawl_one_lead_and_save_json(obj: Lead):

    # check lead source and use functions according to the event type
    crawl_result = None
    if obj.source == LEAD_SOURCES_ENUM.EVENTBRITE:
        crawl_result = eventbrite_events([obj.url], return_string=False, many=False),
    if obj.source == LEAD_SOURCES_ENUM.HNET:
        crawl_result = startSpider([obj.url], HnetEventSpider)[0],
        crawl_result = ScrapyJSONEncoder().encode(crawl_result)
        crawl_result = json.loads(crawl_result)
        print(crawl_result)
    if crawl_result is not None:
        obj.json = crawl_result
        obj.save()

def convert_local_to_utc_start_datetime(lead: Lead):
    tz = lead.originalTimeZone
    # original datetime with timezone
    original_dt = lead.originalStartDateTime.replace(tzinfo=None)
    # dt = lead.originalStartDateTime.replace(tzinfo=tz)
    dt = tz.localize(original_dt)
    # dt = tz.localize(lead.originalStartDateTime)
    utc_dt: datetime.datetime = dt.astimezone(pytz.timezone('UTC'))
    lead.startDateTime = utc_dt
    lead.save()
def sync_lead_with_webinar_and_save(lead: Lead):



    # if original timezone and original start date time are provided. convert it to utc.

    if lead.originalStartDateTime is not None and lead.originalTimeZone is not None:
        convert_local_to_utc_start_datetime(lead)

    # save change again
    lead.save()

    # start syncing to webinar.

    # check if the lead already has an webinar relational entity, if not create one.
    if not hasattr(lead, 'webinar'):
        lead.webinar = Webinar()
        # change lead.webinar.status = False and wait to approval

    # change the webinar visibility to false. change this to active to publish the webinar
    lead.webinar.status = False

    # sync required fields
    lead.webinar.description = lead.description
    lead.webinar.startDateTimeUTC = lead.startDateTime
    lead.webinar.startDateTimeZoneLocal = lead.originalTimeZone
    lead.webinar.title = lead.title

    # sync other non-required fields if exists
    if lead.registrationDeadline:
        lead.webinar.registrationDeadline = lead.registrationDeadline

    # check if source type has adapter, if not, sync only the required fields
    lead = sync_lead_json_with_webinar(lead)


    if lead.startDateTime is None:
        raise ValueError("Lead's start date time cannot be null")

    lead.webinar.originalUrl = lead.url

    lead.webinar = populate_short_url(lead.webinar)



    # lead.webinar.links.add(detail_link)

    # save all changes.
    lead.webinar.save()

    if lead.hostOrganizations:
        for hostOrganization in lead.hostOrganizations.iterator():

            hostOrganization.hostedWebinars.add(lead.webinar)




    # set lead status as active.
    lead.status = True
    lead.save()


    # add lead's url as detail link for the webinar
    detail_link = Link()
    detail_link.type = LINK_TYPE_ENUM.DETAIL
    detail_link.url = lead.url
    detail_link.webinar = lead.webinar
    detail_link.save()



