import logging

import scrapy

from ..items import HnetItem

logger = logging.getLogger(__name__)

class HnetEventSpider(scrapy.Spider):
    name = "hnet_events"

    def __init__(self, *args, **kwargs):
        super(HnetEventSpider, self).__init__(*args, **kwargs)

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
        i = HnetItem()
        i['url'] = response.request.url
        i['title'] =  response.xpath('//div[@class="l-content"]//h1//text()').get()
        i['description'] = "\n".join(response.xpath(
            '//div[contains(@class, "field--type-text-with-summary")]/div[contains(@class, "field__items")]//text()').extract())
        i['startDateTime'] = response.xpath('//span[@class="date-display-single"]/@content').get()
        i['itemType'] = response.xpath(
            '//div[contains(@class, "field--name-field-announcement-type")]/div[contains(@class, "field__item")]//text()').get()
        i['location'] = response.xpath(
            '//div[contains(@class, "field--name-field-announcement-country")]/div[contains(@class, "field__item")]//text()').get()
        i['keywords'] = response.xpath(
            '//div[contains(@class, "field--name-field-subject-fields")]/div[contains(@class, "field__item")]//text()').get()
        i['email'] = response.xpath(
            '//div[contains(@class, "field--name-field-announcement-email")]/div[contains(@class, "field__item")]//text()').get()


        # filename = f'event-{1}.json'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # print(i)
        print(i)
        yield i
