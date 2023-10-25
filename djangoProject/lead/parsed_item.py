from dataclasses import dataclass


@dataclass
class ParsedItem:
    organizationName: any = None
    organizations: any = None
    title: any = None
    description: any = None
    startDateTimeString: any = None
    startDateTimeJson: any = None
    contactEmail: any = None
    contactInfo: any = None
    keywords: any = None
    location: any = None
    eventType: any = None
    eventUrl: any = None
