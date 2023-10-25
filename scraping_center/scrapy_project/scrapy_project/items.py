# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html



import scrapy
from scrapy import Field



class HnetItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    url = Field()
    title = Field()
    itemType = Field()
    startDateTime = Field()
    keywords = Field()
    description = Field()
    eventUrl = Field()
    hnetUrl = Field()
    location = Field()
    email = Field()

class EventbriteViewEventScrapyItem(scrapy.Item):
    events_json = Field()