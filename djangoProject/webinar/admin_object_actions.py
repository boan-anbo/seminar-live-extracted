import datetime

import pytz

from djangoProject.talk.models import Talk
from djangoProject.webinar.models import Webinar


def convert_webinar_local_to_utc_start_datetime(webinar: Webinar, save=True):
    # tz = webinar.startDateTimeZone
    # # original datetime with timezone
    # original_dt = webinar.startDateTimeOriginal.replace(tzinfo=None)
    # dt = tz.localize(original_dt)
    # utc_dt: datetime.datetime = dt.astimezone(pytz.timezone('UTC'))
    # webinar.startDateTime = utc_dt

    webinar.startDateTimeUTC = convert_local_to_utc_start_datetime(webinar.startDateTimeZoneLocal.__str__(), webinar.startDateTimeLocal)
    if save:
        webinar.save()

def convert_local_to_utc_start_datetime(timezone_str: str, dateTime: datetime) -> datetime:
    local_tz = pytz.timezone(timezone_str)
    local_datetime = dateTime.replace(tzinfo=None)
    local_datetime_with_timezone = local_tz.localize(local_datetime)
    utc_dt: datetime = local_datetime_with_timezone.astimezone(pytz.timezone('UTC'))
    return utc_dt

def to_titlecase(webinar: Webinar):

    # check lead source and use functions according to the event type
    webinar.title = webinar.title.title()
    webinar.save()

def make_webinar_only_talk(webinar: Webinar):

    newTalk = Talk()

    newTalk.title = webinar.title

    newTalk.save()

    webinar.talks.add(newTalk)

    webinar.save()