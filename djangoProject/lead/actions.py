import json
import re
from dataclasses import asdict
from typing import cast, Dict

import requests
from bs4 import BeautifulSoup

from djangoProject.lead.parsed_item import ParsedItem
from djangoProject.organization.models import Organization
from djangoProject.organization.serializers import OrganizationSerializer
from djangoProject.sources.const import EventbriteDetail, Module


def get_data_from_eventbrite(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    try:
        html_raw = soup.find("script", text=re.compile('model:\s?{.*},')).__str__()
        html_part = re.findall(r'model:(\s?{.*}),', html_raw)[0]
        model = cast(EventbriteDetail, json.loads(html_part))
        print(json.dumps(model, indent=4))
        start = model['start']
        title=None
        try:
            title = model['name']['text']
        except:
            pass
        print(start)
        print(title)
        paragraph_modules = model['structured_content']['modules']
        html_content = ''
        orgName = None
        try:
            orgName = re.search(r'orgName:(.*),', soup.__str__()).group(1).replace("\"", '').strip()
        except:
            pass
        for module in paragraph_modules:
            module = cast(Module, module)
            if module['type'] == 'text':
                html_content += module['data']['body']['text']
        return asdict(ParsedItem(
            organizationName=orgName,
            title=title,
            description=html_content,
            startDateTimeJson=start,
            organizations=None,
            startDateTimeString=None
        ))
    except:
        raise

def get_data_from_zoom(url: str):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    webinar_topic = soup.find("div", class_="webinar_topic")
    controls = webinar_topic.find_all('div', class_="controls")
    control_length = len(controls)
    print(control_length)
    title = None
    description = None
    time = None
    # organization name
    organization_name = None
    # organization full name
    organization_fullname = []
    #  organization short match.
    organization_short = []
    school_name_matches = re.search(r'https?://(.*).zoom', url)
    if school_name_matches is not None:
        organization_name = school_name_matches.group(1).title()
        if organization_name:
            organization_fullname = Organization.objects.filter(name__contains=organization_name).all()
            organization_name_upper = organization_name.upper()
            print(organization_name_upper)
            organization_short = Organization.objects.filter(nameShort__contains=organization_name_upper).all()
    for i in range(control_length):
        if i == 0:
            title = controls[i].text.strip()
        if i == 1:
            if control_length == 2:
                time = controls[i].text.strip()
            if control_length == 3:
                description = controls[i].decode_contents().strip()

        if i == 2:
            if control_length == 3:
                time = controls[i].text.strip()
    print(time,description, time)
    organization_str = None
    print(organization_short)
    if len(organization_fullname) > 0 or len(organization_short) > 0 :
        organization_str = OrganizationSerializer((organization_fullname | organization_short), many=True).data
        print(organization_str)
    if len(organization_fullname) == 0 or len(organization_short) > 0 and organization_name is not None:
        organization_name = organization_name.title()
    #     as dict because dataclass needs to be converted to Dict to be serialized as json object.
    return asdict(ParsedItem(
        organizations=json.dumps(organization_str),
        organizationName=organization_name,
        title=title,
        description= description,
        startDateTimeString=time,
        startDateTimeJson=None
    ))
# if __name__ == '__main__':
#     get_data_from_eventbrite('https://www.eventbrite.com/e/a-matter-of-death-and-life-irvin-yalom-tickets-130840590729?aff=ebdssbcitybrowse&keep_tld=1')

def get_data_from_hnet(url: str) -> Dict:
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    div = soup.find('div', class_='l-content')
    title = div.find('h1').text
    content_nodes = div.find('div', class_='node__content')

    fields = content_nodes.find_all('div', class_='field')
    startDateTimeString = None
    contactEmail = None
    contactInfo = None
    keywords = None
    location = None
    eventType = None
    eventUrl = None

    for field in fields:
        label_div = field.find('div', class_='field__label')
        if label_div:
            label = label_div.text
            value = field.find('div', class_='field__item').text
            if 'type' in label.lower():
                print('TYPE: ', value)
                eventType = value
            if 'date' in label.lower():
                print('date: ', value)
                startDateTimeString = value
            if 'location' in label.lower():
                print('location: ', value)
                location = value
            if 'subject' in label.lower():
                print('subject: ', value)
                keywords = value
            if 'email' in label.lower():
                print('email', value)
                contactEmail = value
            if 'url' in label.lower():
                print('url', value)
                eventUrl = value
            if 'contact info' in label.lower():
                contactInfo = value
                print('contact info', value)

    content_fields = div.find('div', class_='field--type-text-with-summary').find_all('p')
    all_text_content = None
    for p in content_fields:
        if all_text_content is None:
            all_text_content = ''
        all_text_content += '<p>' + p.decode_contents() + '</p>'
    return asdict(ParsedItem(
        title=title,
        startDateTimeString=startDateTimeString,
        description=all_text_content,
        contactEmail=contactEmail,
        contactInfo=contactInfo,
        keywords=keywords,
        location=location,
        eventType=eventType,
        eventUrl=eventUrl))