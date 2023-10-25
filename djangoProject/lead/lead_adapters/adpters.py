from typing import cast

import dateutil

from djangoProject.lead.const import LEAD_SOURCES_ENUM
from djangoProject.lead.lead_adapters.adpter_schemas.adapter_eventbrite_schema import AdapterEventbriteSchema
from djangoProject.lead.lead_adapters.adpter_schemas.adapter_hnet_schema import AdapterHnetSchemaElement
from djangoProject.lead.models import Lead


def log_match(source_type: str):
    print("matched to ", source_type)

def sync_lead_json_with_webinar(lead: Lead) -> Lead:
    if lead.source == LEAD_SOURCES_ENUM.HNET:
        # log_match(lead.source)
        lead = adapter_hnet(lead)
        return lead

    if lead.source == LEAD_SOURCES_ENUM.EVENTBRITE:
        # log_match(lead.source)
        lead = adapter_eventbrite(lead)
        return lead

    # else return lead
    print("matched no source type")
    return lead



def adapter_eventbrite(lead: Lead) -> Lead:
    eventbrite_event = cast(AdapterEventbriteSchema, lead.json[0])
    print(eventbrite_event)

    # update lead
    lead.startDateTime = dateutil.parser.parse(eventbrite_event['start']['utc'])
    lead.originalStartDateTime = dateutil.parser.parse(eventbrite_event['start']['local'])
    lead.originalTimeZone = eventbrite_event.get('start', 'UTC').get('timezone', 'UTC')
    lead.save()

    lead.webinar.title = eventbrite_event['name']['text']
    lead.webinar.startDateTimeUTC = lead.startDateTime
    lead.webinar.description = eventbrite_event['summary']
    return lead

def adapter_hnet(lead: Lead) -> Lead:
    hnet_event = cast(AdapterHnetSchemaElement, lead.json[0])
    print(hnet_event)
    lead.webinar.title = hnet_event['title']
    # lead.webinar.startDateTime = dateutil.parser.parse(hnet_event['start']['utc'])
    # lead.webinar.startDateTimeZone = hnet_event.get('start', 'UTC').get('timezone', 'UTC')
    lead.webinar.description = hnet_event['description']
    return lead