import multiprocessing

import scrapy
from multiprocessing import Process

from scrapy import signals, Spider
from scrapy.crawler import CrawlerProcess
from threading import Thread
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from scraping_center.scrapy_project.scrapy_project.spiders.hnet import HnetEventSpider

temporary_results = []

def startSpider(urls: [str], spider: Spider):
    # pre_process code
    return run_spider(urls, spider)
    # after_process code

def f(queue, urls: [str], spider: Spider):
    try:
        print("INPUT:" + ",".join(urls))

        # getting result container for the treahd
        results = queue.get()
        # urls = queue.get()
        def crawler_results(signal, sender, item, response, spider):
            results.append(item)
        dispatcher.connect(crawler_results, signal=signals.item_passed)
        process = CrawlerProcess(get_project_settings())
        process.crawl(spider, start_urls=urls)
        process.start()

        # print(results)
        # giving result back to the main thread.
        queue.put(results)
    except Exception as e:
        print(e)



def run_spider(urls: [str], spider: Spider):
    queue = multiprocessing.Queue()
    queue.put(temporary_results)
    p = Process(target=f, args=(queue, urls, spider))
    p.start()
    p.join()
    # fetch result after the thread is done
    final_results = queue.get()
    print(final_results)
    return final_results

# class testThread(Thread):
#     def __init__(self):
#         Thread.__init__(self)
#
#     def run(self):
#         startCrawler()


if __name__ == "__main__":
    t = testThread()
    t.start()

# from scrapy import crawler, signals
# from scrapy.crawler import CrawlerRunner
# from twisted.internet import reactor
#
# from scraping_center.scrapy_project.scrapy_project.spiders.hnet import HnetEventSpider
#
# def run():
#     runner = CrawlerRunner()
#     crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
#     crawler.configure()
#     d = runner.crawl(HnetEventSpider,
#                      start_urls="https://networks.h-net.org/node/73374/announcements/7081399/webinar-yang-shen-self-knowledge-religious-knowledge-lottery")
#     d.addBoth(lambda _: reactor.stop())
#     reactor.run()  # the script will block here until the crawling is finished
#