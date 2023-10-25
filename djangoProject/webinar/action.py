import json
from datetime import datetime

import pytz
from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware
from rest_framework import exceptions, status
from rest_framework.response import Response
from timezone_field import TimeZoneField

from djangoProject.host.models import Host
from djangoProject.lead.models import Lead
from djangoProject.link.const import LINK_TYPE_ENUM
from djangoProject.link.models import Link
from djangoProject.organization.models import Organization
from djangoProject.person.models import Person
from djangoProject.speaker.models import Speaker
from djangoProject.submission.models import Submission
from djangoProject.tag.models import Tag
from djangoProject.userprofile.models import UserProfile
from djangoProject.util_functions.populate_short_url import populate_short_url
from djangoProject.webinar.admin_object_actions import convert_webinar_local_to_utc_start_datetime, \
    convert_local_to_utc_start_datetime
from djangoProject.webinar.const import RECOMMEND_LEVEL
from djangoProject.webinar.models import Webinar

def get_test_time_result(self, request):
    try:
        startDateTimeZone_str = request.data.get('startDateTimeZoneLocal', None)
        print('start Date Time Zone', startDateTimeZone_str)

        startDateTime_str = request.data.get('startDateTimeLocal', None)
        print('start Date Time Local', startDateTime_str)

        if startDateTime_str is None:
            startDateTime_str = request.data.get('startDateTimeUTC', None)
            if startDateTime_str is None:
                raise
            else:
                startDateTimeZone_str = 'UTC'

        year = int(startDateTime_str.get('year'))
        month = int(startDateTime_str.get('month'))
        day = int(startDateTime_str.get('day'))
        hour = int(startDateTime_str.get('hour'))
        minute = int(startDateTime_str.get('minute'))

        startDateTimeLocal = datetime(year, month, day, hour, minute)
        make_aware(startDateTimeLocal)  # current timezone, or...
        make_aware(startDateTimeLocal, timezone=pytz.timezone(startDateTimeZone_str))  # ...specific timezone
        print('Naive Datetime', startDateTimeLocal)

        utc_time: datetime = convert_local_to_utc_start_datetime(startDateTimeZone_str, startDateTimeLocal)
        response = {}
        response['inputTime'] = startDateTimeLocal
        response['inputTimezone'] = startDateTimeZone_str
        response['UTC'] = utc_time
        response['America/Los_Angeles'] = utc_time.astimezone(pytz.timezone('America/Los_Angeles'))
        response['America/Chicago'] = utc_time.astimezone(pytz.timezone('America/Chicago'))
        response['America/New_York'] = utc_time.astimezone(pytz.timezone('America/New_York'))
        response['Europe/London'] = utc_time.astimezone(pytz.timezone('Europe/London'))
        response['Europe/Berlin'] = utc_time.astimezone(pytz.timezone('Europe/Berlin'))
        response['Europe/Moscow'] = utc_time.astimezone(pytz.timezone('Europe/Moscow'))
        response['Asia/Shanghai'] = utc_time.astimezone(pytz.timezone('Asia/Shanghai'))
        response['Asia/Tokyo'] = utc_time.astimezone(pytz.timezone('Asia/Tokyo'))
        response['Australia/Sydney'] = utc_time.astimezone(pytz.timezone('Australia/Sydney'))
        return response
    except Exception as e:
        print(e)
        raise e
def post_webinar_detailed_save(self, request):
    try:
        # get url and description
        originalUrl = request.data.get('originalUrl', None)
        print('url', originalUrl)
        description = request.data.get('description', None)
        print('description', description)

        useStartDateTimeUTC = False

        startDateTimeUTC = request.data.get('startDateTimeUTC', None)
        startDateTimeLocal = request.data.get('startDateTimeLocal', None)

        if startDateTimeUTC is not None:
            useStartDateTimeUTC = True
            startDateTimeUTC = get_start_date_time_utc(request)


        if useStartDateTimeUTC == False:
            if startDateTimeLocal is not None:
                startDateTimeLocal = get_start_date_time_local(request)
            else:
                raise Exception('You need to either provide UTC or Local date. ')

        if useStartDateTimeUTC and startDateTimeLocal:
            raise Exception("You cannot post both Local DateTime and UTC date time. Either provide only local datetime and let the backend calculate UTC for your, or left the Local date time and provide UTC which will be stored as is.")

        startDateTimeZoneLocal_str = request.data.get('startDateTimeZoneLocal', None)

        print('timezone', startDateTimeZoneLocal_str)

        if startDateTimeZoneLocal_str is None:
            raise Exception('You need provide to timezone')

        title = request.data.get('title', None)
        print('title', title)

        if title is None or not (len(title) > 0):

            raise Exception('Empty Title', title)

        tagIds = request.data.get('tagIds', None)

        print('Tag Ids', tagIds)

        hostOrganizationIds = request.data.get('hostOrganizationIds', None)

        print('hostOrganizations', hostOrganizationIds)

        hostIds = request.data.get('hostIds', None)

        print('hostIds', hostIds)


        recommend = int(request.data.get('recommend', None))
        print('recommend', recommend)

        originalUrl = request.data.get('originalUrl', None)
        print('originalUrl', originalUrl)

        id = request.data.get('id', None)
        print('id', id)
        # update toggle
        update = False

        lead_id = request.data.get('leadId', None)

        speakers = request.data.get('participants', None)

        links = request.data.get('links', None)
        print('links', links)

        # whether webinar is active
        webinar_status = request.data.get('status', False)


        if lead_id:
            try:
                id = Webinar.objects.get(lead__id=lead_id).id
                if id:
                    update = True
            except:
                pass

        webinar: Webinar


        if id:
            webinar = Webinar.objects.get(id=id)
            if webinar is None:
                raise
            else:
                webinar.startDateTimeZoneLocal = pytz.timezone(startDateTimeZoneLocal_str)
                webinar.startDateTimeLocal=startDateTimeLocal
                webinar.startDateTimeUTC=startDateTimeUTC
                webinar.title=title
                webinar.description = description
                update = True
        else:
            webinar = Webinar(
            startDateTimeZoneLocal=pytz.timezone(startDateTimeZoneLocal_str),
            startDateTimeLocal=startDateTimeLocal,
            startDateTimeUTC=startDateTimeUTC,
            title=title,
            description=description
            )

        profile = get_object_or_404(UserProfile, user=request.user)
        webinar.creator = profile
        webinar.save()

        if recommend:
            if recommend < 0:
                recommend = 0
            if recommend > 3:
                recommend = 3
            webinar.recommend = recommend



        if links:
            for existing_link in webinar.links.all():
                existing_link.delete()


        for link in links:
            type = getattr(LINK_TYPE_ENUM, link.get('type'), None)
            if type:
                newLink = Link(url=link.get('url'), note=link.get('note'), type=type)
                print(type)
                print('New Link Created', newLink.type)
                webinar.links.add(newLink, bulk=False)
            else:
                raise Exception('New Link Type Error', link)

        if tagIds:
            webinar.tags.clear()
        for tagId in tagIds:
            tag = Tag.objects.get(id=tagId)

            webinar.tags.add(tag)

        if hostOrganizationIds:
            webinar.hostOrganizations.clear()

        for orgId in hostOrganizationIds:
            org = Organization.objects.get(id=orgId)
            webinar.hostOrganizations.add(org)


        if hostIds:
            webinar.hosts.clear()

        for hostId in hostIds:
            host = Host.objects.get(id=hostId)
            webinar.hosts.add(host)


        print('SPEAKER LENGTH:', len(speakers))
        if speakers is not None:
            for existing_speaker in webinar.participants.all():
                existing_speaker.delete()
            for speaker in speakers:
                print('SPEAKER: ', speaker)
                person = speaker['person']
                old_person = None
                new_person_id = person.get('id', None)
                if new_person_id:
                    try:
                        old_person = Person.objects.get(id=new_person_id)
                        print('FOUND OLD PERSON', old_person)
                    except:
                        pass

                firstName = person.get('firstName', None)
                print('FIRSTNAME:', firstName)
                lastName = person.get('lastName', None)
                firstNameCn = person.get('firstNameCn', None)
                lastNameCn = person.get('lastNameCn', None)
                affiliation = speaker.get('affiliation', None)

                new_person = None
                if old_person:
                    if firstName:
                        old_person.firstName = firstName
                    if lastName:
                        old_person.lastName = lastName
                    if firstNameCn:
                        old_person.firstNameCn = firstNameCn
                    if lastNameCn:
                        old_person.lastNameCn = lastNameCn
                    new_person = old_person
                else:
                    try:
                        same_name_person = Person.objects.get(firstName=firstName, lastName=lastName)
                        if same_name_person:
                            new_person = same_name_person
                    except:
                        new_person = Person.objects.create(firstName=firstName, lastName=lastName, firstNameCn=firstNameCn, lastNameCn=lastNameCn)
                new_person.save()
                new_speaker = Speaker.objects.create(affiliation=affiliation, person=new_person)
                webinar.participants.add(new_speaker)


        webinar.status = webinar_status
        print('status', webinar.status)

        webinar.originalUrl = originalUrl
        print('Original Url', webinar.originalUrl)


        if lead_id and update == False:
            if len(lead_id) > 0:
                lead = Lead.objects.get(id=lead_id)
                lead.webinar = webinar
                lead.status = True
                lead.save()


        # webinar = populate_short_url(webinar)
        webinar.save()
        # convert_webinar_local_to_utc_start_datetime(webinar)
        return
    except Exception as e:
        raise e
        # if url is None and description is None:
    #     raise exceptions.ParseError
    #
    # try:
    #     webinar = Webinar()
    #     if url and len(url) > 0:
    #         submission.url = url
    #
    #     if description and len(description) > 0:
    #         submission.description = description
    #
    #     if submission.url or submission.description:
    #         profile = get_profile_by_user(request.user)
    #         submission.status = False
    #         submission.contributor = profile
    #         submission.save()
    #         return Response(status=status.HTTP_200_OK)
    #
    #     else:
    #         raise
    # except:
    #     raise exceptions.ParseError()

def get_start_date_time_local(request) -> datetime:
    startDateTimeZoneLocal_str = request.data.get('startDateTimeZoneLocal', None)
    print('startDateTimeZone Local', startDateTimeZoneLocal_str)

    startDateTimeLocal_str = request.data.get('startDateTimeLocal', None)
    print('startDateTimeLocal', startDateTimeLocal_str)

    year = int(startDateTimeLocal_str.get('year'))
    month = int(startDateTimeLocal_str.get('month'))
    day = int(startDateTimeLocal_str.get('day'))
    hour = int(startDateTimeLocal_str.get('hour'))
    minute = int(startDateTimeLocal_str.get('minute'))

    startDateTimeLocal = datetime(year, month, day, hour, minute)

    make_aware(startDateTimeLocal)  # current timezone, or...
    make_aware(startDateTimeLocal, timezone=pytz.timezone(startDateTimeZoneLocal_str))  # ...specific timezone
    print('Naive Start Datetime Original', startDateTimeLocal)
    return startDateTimeLocal

# get utc from json request: {year, month, day, hour, minute}
def get_start_date_time_utc(request) -> datetime:

    startDateTimeUTC_str = request.data.get('startDateTimeUTC', None)
    print('startDateTimeUTC', startDateTimeUTC_str)

    year = int(startDateTimeUTC_str.get('year'))
    month = int(startDateTimeUTC_str.get('month'))
    day = int(startDateTimeUTC_str.get('day'))
    hour = int(startDateTimeUTC_str.get('hour'))
    minute = int(startDateTimeUTC_str.get('minute'))

    startDateTimeUTC = datetime(year, month, day, hour, minute)

    make_aware(startDateTimeUTC)  # current timezone, or...
    make_aware(startDateTimeUTC, timezone=pytz.timezone('UTC'))  # ...specific timezone
    print('Naive Start Datetime Original', startDateTimeUTC)
    return startDateTimeUTC
