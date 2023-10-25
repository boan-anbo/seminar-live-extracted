import datetime
import json
import re
from typing import List, cast, Type

import requests
from bs4 import BeautifulSoup
from django.utils import dateparse

from djangoProject import settings
# from djangoProject.webinar.models import Webinar
from djangoProject.host.models import Host
from djangoProject.link.const import LinkTypes, LINK_TYPE_ENUM
from djangoProject.link.models import Link
from djangoProject.organization.models import Organization
from djangoProject.sources.actions_test import get_eventbrite_html_by_event_url
from djangoProject.sources.models import Source
from djangoProject.webinar.models import Webinar
from scraping_center.scrapy_project.scrapy_project.models.event_view_item import EventViewItem


def get_eventbrite_organization_url(slugName: str):
    return 'https://www.eventbrite.co.uk/o/' + slugName



def get_future_events_by_slugname(slugName: str) -> List[EventViewItem]:
    url = get_eventbrite_organization_url(slugName)
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    try:
        json_str = soup.find("script", text=re.compile('__SERVER_DATA__')).__str__()
        json_str_part = json_str.partition("window.__SERVER_DATA__ =")[-1]
        json_str_part = json_str_part.partition("</script>")[0]
        print(type(json_str_part))
        # print(json_str_part)
        json_str_part = json_str_part.strip()
        json_str_part = json_str_part.rstrip(';')
        # print(json_str_part[])
        json_object = json.loads(json_str_part)
        future_events = cast(List[EventViewItem], json_object['view_data']['events']['future_events'])

        free_future_events = list(filter(lambda event: event['is_free'] == True and event['online_event'] == True, future_events))

        print(len(free_future_events))
        # event_id = event_id_div[0]['data-eid']
        # return fetch_eventbrite_one_by_id(event_id)
        return free_future_events
    except:
        raise

def save_webinar_from_eventbrite_view_event(e: EventViewItem, source: Source):

    input_eventbrite_event_id = e['id']
    try:
        if Webinar.objects.get(sourcePlatformId=input_eventbrite_event_id):
        # duplucated return
            return
    except:
        pass
    webinar = Webinar()
    webinar.status = False
    try:
        webinar.sourcePlatformId = input_eventbrite_event_id
        webinar.title = e['name']['text']
        webinar.startDateTimeUTC = dateparse.parse_datetime(e['start']['utc'])
        webinar.startDateTimeZoneLocal = e['start']['timezone']


        # webinar.description = e['summary']
        webinar.language = e['language']

        webinar.save()


        for tag in source.tags.all():
            webinar.tags.add(tag)




        detailLink = Link()
        detailLink.type = LINK_TYPE_ENUM.DETAIL
        detailLink.url = e['url']
        detailLink.webinar = webinar
        detailLink.save()

        html_content = get_eventbrite_html_by_event_url(detailLink.url)

        print(html_content)
        webinar.description = html_content

        source.webinars.add(webinar)

        source.save()


        #  load host or organization

        hostId = getattr(source, 'hostId', None)
        print('HOSTID', hostId)

        if hostId:
            host = Host.objects.get(id=hostId)
            if host:
                webinar.hosts.add(host)

        organizationId = getattr(source, 'organizationId', None)
        if organizationId:
            hostOrganization = Organization.objects.get(id=organizationId)
            if hostOrganization:
                webinar.hostOrganizations.add(hostOrganization)
        print('OrganizationId', organizationId)

        # print(json.dumps(e, indent=4))
        print(webinar.startDateTimeUTC)


        # webinar.startDateTime = ''
        webinar.save()
    except:
        name = getattr(e, 'name', '')
        url = getattr(e, 'url', '')
        slugname = getattr(e, 'slugName', '')
        print('soemthing went wrong: ', name, url, slugname)
        pass



#     "start": {
#         "utc": "2021-04-21T16:00:00Z",
#         "date_header": "Upcoming",
#         "timezone": "America/New_York",
#         "local": "2021-04-21T12:00:00",
#         "formatted_time": "12:00 PM"
#     },


# if __name__ == '__main__':
#     events = get_future_events_by_slugname('brown-university-8695100606')
#     # for e in events:
#     #     webinar = get_webinar_from_eventbrite_view_event(e)
#     #     # webinar.save()
#     print(json.dumps(events, indent=4))