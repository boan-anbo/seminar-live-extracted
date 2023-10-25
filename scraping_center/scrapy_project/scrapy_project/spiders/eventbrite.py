import logging

import scrapy
from scrapy.shell import inspect_response

from ..items import HnetItem

logger = logging.getLogger(__name__)

class EventbriteSpider(scrapy.Spider):
    name = "eventbrite_one"


    def __init__(self, *args, **kwargs):
        super(EventbriteSpider, self).__init__(*args, **kwargs)

        self.start_urls = kwargs.get('start_urls')
        if isinstance(self.start_urls, str):
            self.start_urls = [self.start_urls]
        print("Received", self.start_urls)


    def start_requests(self):
        # get auth token
        auth = '{}'.format('2XGFXVEVQUX62UCDIRIQ')

        # set auth token in headers
        headers = {'Authorization': 'BEARER {}'.format(auth)}

        for one_url in self.start_urls:
            yield scrapy.Request(url=one_url, headers=headers, callback=self.parse)

    # start_urls=['http://www.google.com']
    # def start_requests(self):
    #     logger.info("Start Urls", self.start_urls)
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        # i = ()
        # i['url'] = response.request.url
        # i['title'] =  response.xpath('//h1[@data-automation="listing-title"]//text()').get()
        # print(response)
        inspect_response(response, self)
        # print(response)
        # i['description'] = "\n".join(response.xpath(
        #     '//div[contains(@class, "field--type-text-with-summary")]/div[contains(@class, "field__items")]//text()').extract())
        # i['startDateTime'] = response.xpath('//span[@class="date-display-single"]/@content').get()
        # i['itemType'] = response.xpath(
        #     '//div[contains(@class, "field--name-field-announcement-type")]/div[contains(@class, "field__item")]//text()').get()
        # i['location'] = response.xpath(
        #     '//div[contains(@class, "field--name-field-announcement-country")]/div[contains(@class, "field__item")]//text()').get()
        # i['keywords'] = response.xpath(
        #     '//div[contains(@class, "field--name-field-subject-fields")]/div[contains(@class, "field__item")]//text()').get()
        # i['email'] = response.xpath(
        #     '//div[contains(@class, "field--name-field-announcement-email")]/div[contains(@class, "field__item")]//text()').get()


        # filename = f'event-{1}.json'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # print(i)
        # print(i)
        # yield i
