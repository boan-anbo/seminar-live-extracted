import json
import logging
import os

import django_rq
import ujson
from django.utils.log import configure_logging
from modernrpc.core import rpc_method
from scrapy import cmdline
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet import reactor

from scraping_center.apis.eventbrite import fetch_eventbrite_one_by_url
from scraping_center.scrapy_project.scrapy_project.spiders.hnet import HnetEventSpider
from scraping_center.scrapy_project.run_scrape_spiders import  startSpider

logger = logging.getLogger(__name__)

@rpc_method
def sc_health(urls: [str]):
    print("Initially Received", urls[0])
    #
    # test = "https://networks.h-net.org/node/73374/announcements/7081399/webinar-yang-shen-self-knowledge-religious-knowledge-lottery"
    # cmdline.execute(f'scrapy crawl hnet_events -a start_urls="{test}" -o output.json'.split())
    result = startSpider(urls)
    return ScrapyJSONEncoder().encode(result)

    # def run_spider():

@rpc_method
def eventbrite_events(urls: [str], return_string: bool = True, many: bool = True):
    """

    :param urls:
    :param return_string:
    :param many: whether there is only one input and the return
    :return:
    """
    all_results = []
    # if event_id is not None:
    #     result = fetch_eventbrite_one(event_id)
        # print(result)
    for url in urls:
        all_results.append(fetch_eventbrite_one_by_url(url))
    if not many:
        all_results = all_results[0]

    if return_string:
        return ScrapyJSONEncoder().encode(all_results)
    return all_results
