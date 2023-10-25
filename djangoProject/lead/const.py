from typing import Type

from scraping_center.scrapy_project.scrapy_project.items import HnetItem


class LEAD_SOURCES_ENUM:
    WEB = 'WEB'
    HNET = 'HNET'
    EVENTBRITE = 'EVENTBRITE'

    def getHnetItem(self) -> Type[HnetItem]:
        return HnetItem

LeadSources = [
    (LEAD_SOURCES_ENUM.EVENTBRITE, LEAD_SOURCES_ENUM.EVENTBRITE),
    (LEAD_SOURCES_ENUM.HNET, LEAD_SOURCES_ENUM.HNET),
    (LEAD_SOURCES_ENUM.WEB, LEAD_SOURCES_ENUM.WEB)
]
