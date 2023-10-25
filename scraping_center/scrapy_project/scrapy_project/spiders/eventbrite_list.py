import json
import logging
from typing import cast

from scrapy.utils.serialize import ScrapyJSONEncoder

from ..models.event_view_item import EventViewItem
import scrapy

from ..items import HnetItem, EventbriteViewEventScrapyItem

logger = logging.getLogger(__name__)

class EventbriteListSpider(scrapy.Spider):
    name = "eventbrite-list"


    def __init__(self, *args, **kwargs):
        super(EventbriteListSpider, self).__init__(*args, **kwargs)

        self.start_urls = kwargs.get('start_urls')
        print("Received", self.start_urls)

    def start_requests(self):
        # urls = ['http://example.com/']

        for one_url in self.start_urls:
            yield scrapy.Request(url=one_url, callback=self.parse)
    # start_urls=['http://www.google.com']
    # def start_requests(self):
    #     logger.info("Start Urls", self.start_urls)
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):

        print(response)
        json_str = response.xpath("//script[contains(., '__SERVER_DATA__ ')]//text()").get()
        json_str_part = json_str.partition("window.__SERVER_DATA__ =")[-1]
        json_str_part = json_str_part.strip()
        json_str_part = json_str_part.rstrip(';')
        json_object = json.loads(json_str_part)
        organization = (json_object['jsonld'][0])
        organization_color = ['jsonld']
        future_events = json_object['view_data']['events']['future_events']

        i = EventbriteViewEventScrapyItem()
        # result =
        # print(result)
        i['events_json'] = 'ffffffffffffffffffffffffffffff'
        # print(json.dump(future_events))
        yield i
        # filename = f'event-{1}.json'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # print(i)

