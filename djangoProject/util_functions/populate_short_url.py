# from django.utils.text import slugify

# i18 version 3rd party slugify

from uuslug import slugify

from djangoProject.webinar.models import Webinar

# fixme slugTitle doesn't support parsing Chinese characters.
def populate_short_url(webinar: Webinar) -> Webinar:
    slugTitle = slugify(webinar.startDateTimeUTC.strftime("%Y-%m-%d") + '_' + webinar.title)
    webinarsWithSameTitle = Webinar.objects.filter(shortUrl=slugTitle).exclude(id=webinar.id)
    if len(webinarsWithSameTitle) > 0:
        counter = 1
        slugTitle = slugTitle + '_' + str(counter)
        webinarsWithSameTitle = Webinar.objects.filter(shortUrl=slugTitle)
        while len(webinarsWithSameTitle) > 0:
            counter += 1
            slugTitle = slugTitle + '_' + str(counter)
            webinarsWithSameTitle = Webinar.objects.filter(shortUrl=slugTitle)
    webinar.shortUrl = slugTitle
    return webinar


