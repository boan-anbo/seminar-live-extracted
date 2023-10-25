import datetime
import time

from django_extensions.management.jobs import BaseJob, QuarterHourlyJob

from djangoProject.common.time_utils.sl_time import get_all_times, get_local_from_utc, get_est, get_pst, get_cst, \
    get_gmt
from djangoProject.tag.models import Tag
from djangoProject.twitterrecord.models import TwitterRecord
from djangoProject.webinar.filters import WebinarFilter
from djangoProject.webinar.models import Webinar
from sl2_connect.twitter.test import tweet, remove_tweet, get_my_tweets



class Job(QuarterHourlyJob):
    help = "Quarter Hourly Job."

    def execute(self):
        # print(response)
        # executing empty sample job
        webinars = get_tomorrow_webinars_to_tweet().all()
        count = 0
        # tweetWebinar(webinars.first())
        for webinar in webinars:
        #     print(webinar.startDateTimeUTC)
            try:
                tweetWebinar(webinar, print_only=True)
                count += 1
                time.sleep(15)
            finally:
                continue
        # # print('text')
        #
        # print('DONE Tweeted ', count)

def get_sl_event_link(shortUrl: str):
    return 'https://www.seminar-live.com/detail/' + shortUrl



def tweetWebinar(webinar: Webinar, print_only=False):
    try:
        if (webinar.twitterRecords.count() > 0 and not print_only):
            print('webinar already tweeted')
            raise Exception("Webinar ALredy Tweeted")
        title = webinar.title
        tz = webinar.startDateTimeZoneLocal.__str__()
        time = webinar.startDateTimeUTC
        local_datetime = get_local_from_utc(time, tz)
        local_str = get_date_time_str_with_date(local_datetime) + ' (' + tz.replace('_', ' ') + ')'

        est_str = get_date_time_str_time_only(get_est(time)) + ' (EST)'

        pst_str = get_date_time_str_time_only(get_pst(time)) + ' (PST)'

        cst_str = get_date_time_str_time_only(get_cst(time)) + ' (CST)'

        gmt_str = get_date_time_str_time_only(get_gmt(time)) + ' (GMT)'

        tags_str = get_hash_tags(webinar.tags.all())

        url = get_sl_event_link(webinar.shortUrl)

        speakers = webinar.participants.all()

        speakers_str = get_speaker_names(speakers)

        main_tweet_text = "{speakers_str}{title}\n{local_str} {est_str} {pst_str} {cst_str} {gmt_str}\n{tags_str}".format(
            speakers_str=speakers_str,
            title=title,
            local_str=local_str,
            tags_str=tags_str,
            est_str=est_str,
            pst_str=pst_str,
            cst_str=cst_str,
            gmt_str=gmt_str
            # tags_str=tags_str +' 2'
        )

        print('LENGTH:', len(main_tweet_text))
        print(main_tweet_text)
        main_tweet_response = tweet(main_tweet_text)

        main_tweet_id = main_tweet_response.id_str


        if main_tweet_id and not print_only:
            new_tr = TwitterRecord(tweetId=main_tweet_id, webinar=webinar, inReplyToTargetId=None)
            new_tr.save()
        url_tweet_response = post_url(url, main_tweet_id)

        url_tweet_response_id = url_tweet_response.id_str

        if url_tweet_response_id and not print_only:
            new_url_tr = TwitterRecord(tweetId=main_tweet_id, webinar=webinar, inReplyToTargetId=url_tweet_response_id)
            new_url_tr.save()
    except Exception as e:
        print(e)
        raise
    # print('response', response)
    # print(content_text)

# def get_webinar_time(webinar: Webinar):
#     return get_all_times(webinar.startDateTimeUTC, localTimezone=)

def post_url(url, in_reply_to):
    return tweet('See: ' + url, in_reply_to)

def get_date_time_str_with_date(dt: datetime):
    return dt.strftime("%m-%d %H:%M")

def get_date_time_str_time_only(datetime: datetime):
    return datetime.strftime("%H:%M")

def get_hash_tags(tags):
    tags_str = ''
    for tag in tags:
        tagName = tag.name
        tagName = "".join(tagName.split())
        tags_str += '#' + tagName + ' '

    return tags_str.strip()

def get_speaker_names(speakers):
    speakers_str = ''

    for index, speaker in enumerate(speakers):
        if index >= 1 and index <= 3:
            speakers_str += ', '
        speakers_str += speaker.person.__str__()
        if index == 3 and len(speakers) > 3:
            speakers_str += ' & others'
            break
    if len(speakers_str.strip()) > 0:
        speakers_str += ': '
    return speakers_str

def get_12h_webinars_to_tweet():
    qs = Webinar.objects.filter(recommended=True).all()
    now = datetime.datetime.now()
    next_24h = now + datetime.timedelta(hours=12)
    next_26h = now + datetime.timedelta(hours=14)
    f = WebinarFilter({'startDateTimeUTC_after': next_24h, 'startDateTimeUTC_before': next_26h}, qs)
    return f.qs

def get_tomorrow_webinars_to_tweet():
    qs = Webinar.objects.filter(recommended=True).all()
    now = datetime.datetime.now()
    next_24h = now + datetime.timedelta(hours=12)
    next_26h = now + datetime.timedelta(hours=24)
    f = WebinarFilter({'startDateTimeUTC_after': next_24h, 'startDateTimeUTC_before': next_26h}, qs)
    return f.qs

if __name__ == '__main__':
    job = Job()
    job.execute()