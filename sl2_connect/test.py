import re
from dataclasses import asdict

import requests
from bs4 import BeautifulSoup

from djangoProject.lead.parsed_item import ParsedItem


def test(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    div = soup.find('div', class_='l-content')
    title = div.find('h1').text
    content_nodes = div.find('div', class_='node__content')

    fields = content_nodes.find_all('div', class_='field')
    startDateTimeString = None
    description = None
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
    all_text_content = ''
    for p in content_fields:
        all_text_content += '<p>' + p.decode_contents() + '</p>'
    return asdict(ParsedItem(
        title=title,
        startDateTimeString=startDateTimeString,
        contactEmail=contactEmail,
        contactInfo=contactInfo,
        keywords=keywords,
        location=location,
        eventType=eventType,
        eventUrl=eventUrl
    ))

if __name__ == '__main__':
    test('https://networks.h-net.org/node/73374/announcements/7344629/lecture-renata-holod-visual-and-material-culture-rayy-revealed')