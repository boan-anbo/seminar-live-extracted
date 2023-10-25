from djangoProject.settings import MAIN_DOMAIN_NAME
from djangoProject.webinar.models import Webinar



def get_tweet_text_content(webinar: Webinar):
    try:
        content_text = "{title} starts in one hour at {time_str}. {url} ".format(title=webinar.title, time_str=webinar.startDateTimeUTC.astimezone(), url=get_webinar_url(webinar.shortUrl))
        print(content_text)
    except:
        raise


def get_webinar_url(webinar_short_id: str):
    return MAIN_DOMAIN_NAME + '/' + 'detail/' + webinar_short_id


