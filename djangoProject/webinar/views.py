# Create your views here.
import datetime
import logging
from typing import cast

import pytz
from django.db.models import QuerySet, Prefetch
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.utils.decorators import method_decorator
from django.utils.timezone import make_aware
from django.views.decorators.cache import cache_page
from django_extensions.db.models import ActivatorModel
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from djangoProject.host.models import Host
from djangoProject.host.serializers import HostSerializer
from djangoProject.link.const import LINK_TYPE_ENUM
from djangoProject.link.models import Link
from djangoProject.note.models import Note
from djangoProject.organization.models import Organization
from djangoProject.organization.serializers import OrganizationSerializer
from djangoProject.person.models import Person
from djangoProject.submission.models import Submission
from djangoProject.tag.models import Tag
from djangoProject.tag.serializers import TagSerializer
from djangoProject.taggingrecord.models import TaggingRecord
from djangoProject.taggingrecord.serializers import TaggingRecordSerializer
from djangoProject.userprofile.actions import get_profile_by_user
from djangoProject.userprofile.models import UserProfile
from djangoProject.userprofile.serializers import UserProfileSerializer
from djangoProject.util_functions.populate_short_url import populate_short_url
from djangoProject.webinar.action import post_webinar_detailed_save, get_test_time_result
from djangoProject.webinar.admin_object_actions import convert_local_to_utc_start_datetime, \
    convert_webinar_local_to_utc_start_datetime
from djangoProject.webinar.const import FILTER_TYPE_ENUM
from djangoProject.webinar.filters import WebinarFilter
from djangoProject.webinar.models import Webinar
from djangoProject.webinar.permission import WebinarPermission
from djangoProject.webinar.persmission_custom import IsWebinarTagger, IsRecommender, IsDirectPoster
from djangoProject.webinar.serializers import WebinarSerializer

from django.db.models import Q

# 15s
VIEW_CACHE_EXPIRE_3S = 3

# 15s
VIEW_CACHE_EXPIRE_15S = 15


# 30s
VIEW_CACHE_EXPIRE_30S = 30


# 1m
VIEW_CACHE_EXPIRE_1M = 60 * 1

# 10 minutes
VIEW_CACHE_EXPIRE_5M = 60 * 5

# 10 minutes
VIEW_CACHE_EXPIRE_10M = 60 * 10

# 30m minutes
VIEW_CACHE_EXPIRE_30M = 60 * 30

# 1 day
VIEW_CACHE_EXPIRE_1D = 60 * 60 * 24

# Get an instance of a logger

logger = logging.getLogger(__name__)


# update hasRecordingOrTranscript based on the links
@receiver(post_save, sender=Link)
def update_webinar_links(sender, instance, **kwargs):
    if hasattr(instance, '_dirty'):
        return
    link = cast(Link, instance)
    # if the current webinar's recording/transcript boolean is true.
    oldHas = link.webinar.hasRecordingOrTranscript
    newHas = link.type == LINK_TYPE_ENUM.TRANSCRIPT or link.type == LINK_TYPE_ENUM.RECORDING

    if oldHas != newHas:
        link.webinar.hasRecordingOrTranscript = newHas

        # this solves the post save recursion issue
        # try:
        #     instance._dirty = True
        #     instance.save()
        # finally:
        #     del instance._dirty
    # update registration status
    # oldRequiresStatus = link.webinar.requiresRegistration
    # newRequiresStatus = link.type == LINK_TYPE_ENUM.REGISTERATION
    # if oldRequiresStatus != newRequiresStatus:
    if link.type == LINK_TYPE_ENUM.REGISTRATION:
        link.webinar.requiresRegistration = True

    link.webinar.save()


@receiver(post_delete, sender=Link)
def update_webinar_links_on_delete(sender, instance, **kwards):
    try:
        link = cast(Link, instance)
        if link.type == LINK_TYPE_ENUM.REGISTRATION:
            webinar = Webinar.objects.get(id=link.webinar.id)
            if webinar:
                webinar.requiresRegistration = False
                webinar.save()
    except Exception as e:
        print('Webinar already deleted when the link is deleted', e)
        pass

# DEPRECATED IN FAVOR OF THE PRESAVE METHOD BELOW
# # update webinar short url on create
# @receiver(post_save, sender=Webinar)
# def update_webinar_shorturl(sender, instance, **kwargs):
#     if kwargs.get('created', False):
#         webinar = populate_short_url(instance)
#         webinar.save()
#
#     print("short_url_updated")


# update webinar short url on create
@receiver(pre_save, sender=Webinar)
def update_webinar_shorturl(sender, instance: Webinar, **kwargs):
    if hasattr(instance, '_dirty'):
        return
    # update start date time local
    if instance.startDateTimeLocal is not None:
        convert_webinar_local_to_utc_start_datetime(instance, save=False)
        print("Webinar start date updated ")

    # create shorturl if there is none
    if instance.title and len(instance.title) > 0 and len(instance.shortUrl) == 0:
        instance = populate_short_url(instance)

    # update tag count

    if instance.id is not None:
        if  instance.tags.exists():
            instance.tagCount = instance.tags.count()
        else:
            instance.tagCount = 0
        # tag counnt updated

    # update recommended
    if instance.recommend > 0:
        instance.recommended = True
    else:
        instance.recommended = False



class WebinarViewSet(viewsets.ModelViewSet):
    # Product.objects.prefetch_related(Prefetch(
    #     'likes',
    #     queryset=Like.objects.filter(like=True)))
    queryset = Webinar.objects.filter(status=ActivatorModel.ACTIVE_STATUS).prefetch_related(
        'tags', 'hostOrganizations', 'hosts', 'participants', 'links', 'talks',
        Prefetch('notes', queryset=Note.objects.filter(status=True))).order_by('startDateTimeUTC')
    serializer_class = WebinarSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_fields = ('title',)
    # generic filters for viewset.
    filterset_class = WebinarFilter
    permission_classes = [WebinarPermission]

    # # handle today webinars requests
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def mine(self, request):
        profile = get_profile_by_user(request.user)
        webinars = self.queryset.filter(savedBy=profile)
        # print(request.user)
        # if request.user.isAuthencated:
        #     print("legi user")
        # webinars_str = self.get_serializer(webinars, many=True).data
        return self.return_filtered_and_paginated_qs(webinars)

    # extra actions for complex queries for webinars.

    # get five more recent webinars added
    @method_decorator(cache_page(VIEW_CACHE_EXPIRE_10M))
    @action(detail=False, methods=['get'], permission_classes=[])
    def latest_events(self, request, *args, **kwargs):
        qs = self.queryset.order_by('-created')[:5]
        webinars_str = self.get_serializer(qs, many=True).data
        return Response(webinars_str)



    # get five more recent webinars with recordings
    @method_decorator(cache_page(VIEW_CACHE_EXPIRE_10M))
    @action(detail=False, methods=['get'], permission_classes=[])
    def latest_recordings(self, request, *args, **kwargs):
        qs = self.queryset.filter(hasRecordingOrTranscript=True).order_by('-created')[:10]
        webinars_str = self.get_serializer(qs, many=True).data
        return Response(webinars_str)

    # retrive webinars by json array of ids, mainly for unloggedin users to retrieve webinars that are saved locally;
    @action(detail=False, methods=['post'], permission_classes=[])
    def ids(self, request: Request):
        try:
            ids = request.data['ids']
            webinars = self.queryset.filter(id__in=ids)
            return self.return_filtered_and_paginated_qs(webinars)
        except:
            raise

    # handle today webinars requests
    @method_decorator(cache_page(VIEW_CACHE_EXPIRE_5M))
    @action(detail=False, methods=['get'], permission_classes=[])
    def today(self, request, *args, **kwargs):
        print(request.LANGUAGE_CODE)
        # filter by today
        qs = self.get_today_webinars(request)
        # paginate results
        return self.return_filtered_and_paginated_qs(qs)

    # handle today webinars requests
    # @method_decorator(cache_page(VIEW_CACHE_EXPIRE_3S))
    @action(detail=False,
            methods=['post'],
            permission_classes=[IsRecommender])
    def day_recommend(self, request):
        try:
            year = request.data['year']
            month = request.data['month']
            day = request.data['day']
            timezone_str = request.data['timezone']
            range = request.data.get('range', None)

            target_timezone = pytz.timezone(timezone_str)
            target_day_start = target_timezone.localize(datetime.datetime(year, month, day, 0, 0, 0))


            target_day_end = None
            if range is not None and range > 1:
                target_day_end = target_day_start + datetime.timedelta(days=range, hours=24)
            else:
                target_day_end = target_day_start + datetime.timedelta(hours=24)
            # filter by today
            print(target_day_start.__str__())
            print(target_day_end.__str__())
            qs = self.get_day_recommend_webinars(request, target_day_start, target_day_end)

            qs = qs.filter(recommended=True).order_by('recommended')

            qs = self.filter_queryset(qs)

            qs_str = self.get_serializer(qs, many=True).data
            #
            # # responding
            return_data = {}
            #
            return_data['count'] = len(qs)
            return_data['results'] = qs_str
            return_data['next'] = ''
            return_data['previous']=''
            return_data['after'] = target_day_start.__str__()
            return_data['before'] = target_day_end.__str__()
            return_data['timezone'] = timezone_str

            # return self.return_filtered_and_paginated_qs(qs)
            return Response(return_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # handle week webinars request
    @method_decorator(cache_page(VIEW_CACHE_EXPIRE_30M))
    @action(detail=False, methods=['get'], permission_classes=[])
    def week(self, request):
        qs = self.get_week_webinars(request)
        # paginate results
        return self.return_filtered_and_paginated_qs(qs)

    # handle week webinars request
    #  cache requested url for 10 minutes.
    @method_decorator(cache_page(VIEW_CACHE_EXPIRE_30M))
    @action(detail=False,
            methods=['get'],
            permission_classes=[])
    def month(self, request):

        qs = self.get_month_webinars(request)
        # paginate results
        return self.return_filtered_and_paginated_qs(qs)

    # handle week webinars request
    #  cache requested url for 1 hours.
    # @method_decorator(cache_page(60*60*1))
    # @action(detail=False, methods=['get'], permission_classes=[])
    # def month_uncached(self, request):
    #
    #     qs = self.get_month_webinars(request)
    #     # paginate results
    #     return self.return_filtered_and_paginated_qs(qs)

    # handle archive webinars request
    @action(detail=False, methods=['post'], permission_classes=[])
    def archive(self, request):
        # get all saved webinars by profile id
        # this requires POST method
        qs = self.get_webinars_by_profileId_or_ids(request)
        # paginate results
        # filtered_qs = WebinarFilter(qs)

        # further filter by main filter
        qs = self.get_webinars_by_main_filter(request, qs)


        # then use default filterSet to handle other filters like tags, startdatetime or organizers
        qs = self.filter_queryset(qs)
        return self.return_filtered_and_paginated_qs(qs)

    # fetch webinar given short url
    # caching 1 min
    @method_decorator(cache_page(VIEW_CACHE_EXPIRE_15S))
    @action(
        detail=False,
        methods=['get'],
        url_path='short_url/(?P<short_url>[^/.]+)',
        permission_classes=[])
    def get_by_short_url(self, request, short_url):
        webinar = self.queryset.get(shortUrl=short_url)
        webinars_str = self.get_serializer(webinar, many=False).data
        return Response(webinars_str)

    @method_decorator(cache_page(VIEW_CACHE_EXPIRE_10M))
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[]
    )
    def get_all_filters(self, request):
        tags = Tag.objects.all()
        organizations = Organization.objects.all()
        hosts = Host.objects.all()

        all_filters = {}
        all_filters['tags'] = TagSerializer(tags, many=True).data
        all_filters['organizations'] = OrganizationSerializer(organizations, many=True).data
        all_filters['hosts'] = HostSerializer(hosts, many=True).data
        return Response(all_filters)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def post_note(self, request, pk=None):
        try:
            webinar = self.get_object()
            profile = get_profile_by_user(request.user)
            # content = getattr(request.data, 'content', None)

            content = request.data['content']
            isAnonymous = request.data['isAnonymous']
            new_note = Note()
            new_note.status = False
            new_note.webinar = webinar
            new_note.content = content
            new_note.isAnonymous = isAnonymous
            new_note.author = profile
            new_note.save()
            return Response(status=status.HTTP_200_OK)
        except:
            raise exceptions.ParseError()

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def post_webinar(self, request):
        url = request.data.get('url', None)
        description = request.data.get('description', None)
        if url is None and description is None:
            raise exceptions.ParseError

        try:
            submission = Submission()
            if url and len(url) > 0:
                submission.url = url

            if description and len(description) > 0:
                submission.description = description

            if submission.url or submission.description:
                profile = get_profile_by_user(request.user)
                submission.status = False
                submission.contributor = profile
                submission.save()
                return Response(status=status.HTTP_200_OK)

            else:
                raise
        except:
            raise exceptions.ParseError()


    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsDirectPoster]
    )
    def post_webinar_detailed(self, request):
        try:
            post_webinar_detailed_save(self,request)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print('Error post detailed webinar: ', e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


    @action(
        detail=True,
        methods=['get'],
        permission_classes=[IsAuthenticated, IsDirectPoster]
    )
    def get_webinar_detailed(self, request, pk=None):
        try:
            webinar = Webinar.objects.get(id=pk)
            webinar_str = WebinarSerializer(webinar, many=False).data
            return Response(webinar_str, status=status.HTTP_200_OK)
        except Exception as e:
            print('Error post detailed webinar: ', e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsDirectPoster]
    )
    def post_webinar_detailed_test_time(self, request: Request):
        response = get_test_time_result(self, request)
        return Response(response, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def update_note(self, request, pk=None):
        try:
            note_id = request.data['id']
            profile = get_profile_by_user(request.user)
            content = request.data['content']
            isAnonymous = request.data['isAnonymous']
            note_to_update = Note.objects.get(id=note_id)
            if note_to_update.author.id == profile.id:
                note_to_update.content = content
                note_to_update.isAnonymous = isAnonymous
                note_to_update.status = False
                note_to_update.save()
                return Response(status=status.HTTP_200_OK)
            else:
                raise exceptions.AuthenticationFailed
        except:
            raise exceptions.ParseError()

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def delete_note(self, request, pk=None):
        try:
            note_id = request.data['id']
            profile = get_profile_by_user(request.user)
            note_to_delete = Note.objects.get(id=note_id)
            if note_to_delete.author.id == profile.id:
                note_to_delete.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                raise exceptions.AuthenticationFailed
        except:
            raise exceptions.ParseError()

    # get latest tags of an webinar along with all tagging records
    # @method_decorator(cache_page(cache=None, timeout=60))
    @action(
        detail=False,
        methods=['get'],
        url_path='tagging/(?P<short_url>[^/.]+)',
        permission_classes=[IsAuthenticated, IsWebinarTagger]
    )
    def get_all_webinar_tags_by_short_url(self, request, short_url):
        webinar: Webinar = get_object_or_404(Webinar, shortUrl=short_url)

        ids = []
        for tag in webinar.tags.all():
            ids.append(tag.id)

        orgId = None
        if webinar.hostOrganizations.exists():
            orgId = webinar.hostOrganizations.first().id

        response = {}

        response['orgId'] = orgId
        response['tagIds'] = ids
        response['taggingRecords'] = TaggingRecordSerializer(webinar.taggingRecords.all(), many=True).data

        return Response(response, status=status.HTTP_200_OK)

    # tag a webinar
    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsWebinarTagger]
    )
    def tagging(self, request, pk=None):
        try:
            ids = request.data['tagIds']

            webinar = Webinar.objects.get(id=pk)
            tags = Tag.objects.filter(id__in=ids)

            orgId = request.data.get('orgId', None)



            # if the new tags are the same as the latest tags: return error
            if set(tags) == set(webinar.tags.all()) and orgId is None:
                return Response(status=status.HTTP_409_CONFLICT)

            if set(tags) != set(webinar.tags.all()):
                webinar.tags.clear()
                tags = Tag.objects.filter(id__in=ids)
                for tag in tags:
                    webinar.tags.add(tag)
            # print(pk)
            if orgId:
                org = Organization.objects.get(id=orgId)
                webinar.hostOrganizations.clear()
                webinar.hostOrganizations.add(org)

            webinar.save()

            profile = get_profile_by_user(request.user)

            taggingRecord = TaggingRecord.objects.create(webinar=webinar, userprofile=profile)
            #
            for tag in tags:
                taggingRecord.tags.add(tag)
            # taggingRecord.webinar = webinar
            # taggingRecord.save()
            taggingRecord.save()



            # response['tagIds'] = ids
            # response['taggingRecords'] = TaggingRecordSerializer(webinar.taggingRecords.all(), many=True).data

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    #
    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsRecommender]
    )
    def recommend(self, request, pk=None):
        try:
            recommend_level = int(request.data['recommendLevel'])
            if recommend_level < 0:
                recommend_level = 0
            if recommend_level > 3:
                recommend_level = 3

            webinar = Webinar.objects.get(id=pk)
            webinar.recommend = recommend_level
            webinar.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_webinars_by_main_filter(self, request: Request, qs: QuerySet):
        # if profile is provided.
        main_filter_type = request.query_params.get('main_filter_type')
        main_filter_slugname = request.query_params.get('main_filter_slugname')

        if main_filter_type and main_filter_slugname:
            # check if the requested profile id matched the auth user
            try:
                if main_filter_type == FILTER_TYPE_ENUM.HOST:
                    mainFilter = Host.objects.get(slugName=main_filter_slugname)
                    if mainFilter:
                        qs = qs.filter(hosts__id=mainFilter.id)
                    else:
                        raise

                if main_filter_type == FILTER_TYPE_ENUM.TAG:
                    mainFilter = Tag.objects.get(slugName=main_filter_slugname)
                    if mainFilter:
                        qs = qs.filter(tags__id=mainFilter.id)
                    else:
                        raise
                if main_filter_type == FILTER_TYPE_ENUM.SPEAKER_PERSON:
                    mainFilter = Person.objects.get(slugName=main_filter_slugname)
                    if mainFilter:
                        qs = qs.filter(Q(talks__speakers__person__id=mainFilter.id) | Q(participants__person__id=mainFilter.id))
                        # qs = qs.filter(participants_id=mainFilter.id)

                    else:
                        raise
                # I think it's possible to improve performance by retriving webinars from the reverse side, i.e. as the related objects of Organization. Rather than, filtering on the webinar's side
                if main_filter_type == FILTER_TYPE_ENUM.HOST_PARENT_ORGANIZATION:
                    mainFilter = Organization.objects.get(slugName=main_filter_slugname)
                    if mainFilter:
                        qs = qs.filter(hosts__organizations=mainFilter.id)
                    else:
                        raise
                # this one is the direct organization, not the one above hosts.
                # fixme fixed "get_by_main_filter" view to make the main filter type 'hostOrganizations' to search for both direct hostOrganizations and hosts' parent organizations. But the issue is that I need to enforce two things to make this even easier: (1) front end only use 'hostOrganizations'. (2) on the backend, "get_by_main_filter" only handles DIRECT hostorganizations. All the hosts' organizations need to be synced to the DIRECT host organizations field. Meaning the DIRECT organizations can be either: 1. THE ONLY HOST ORGANIZATIONS for convenience (otherwise we should specify host orgnization) and AT THE SAME TIME 2. THE DUPLICATE organization if there is a host with its parent organizations. The later should be done with scripts. This way, I can be rest assured to display either host as hosts (without organizations even though hosts do have the data) and organizations, via the DIRECT hostOrganizations field, as separate, even though possble duplicated fields.
                # for now the only query not working is hosts' parent organizations as secondary filter because secondary filters are handled by Django's viewset and if I use the query 'hostOrganization', django's query will only check direct hostOrganizations (as it should actually). Duplicate hosts' parent organizations and direct organizations have the benefit of leaving computation to the creation phase and when it's loaded, I can just use the direct organizations without worrying about whether I covered the cases where the organizations are used not directly but as the hosts' parent organizations.
                if main_filter_type == FILTER_TYPE_ENUM.HOST_ORGANIZATION:
                    mainFilter = Organization.objects.get(slugName=main_filter_slugname)
                    if mainFilter:
                        qs = qs.filter(Q(hosts__organizations=mainFilter.id) | Q(hostOrganizations=mainFilter.id))
                    else:
                        raise

            except:
                raise exceptions.NotFound()
        # if profile.id.__str__() == profileId:
        #     qs = self.queryset.filter(savedBy=profile)
        # else:
        #     qs = self.get_queryset()

        else:
            qs = self.get_queryset()

        return qs

    # filter webinars by range
    def get_webinars_by_range(self, request: Request, before: str, after: str) -> QuerySet:
        # if 'profile_id' is provided as a parameter, it signifies the intention to filter by profile first. otherwise use all webinars
        qs = self.get_webinars_by_profileId_or_ids(request)

        # further filter by main filter
        qs = self.get_webinars_by_main_filter(request, qs)

        # then filter by time
        logger.error(f'events between {before} and {after}')
        # qs = self.filter_queryset(self.get_queryset())
        f = WebinarFilter({'startDateTimeUTC_after': before, 'startDateTimeUTC_before': after}, qs)
        return f.qs

    # filter by profile Id. must be the first filter, because it defaults to the whole model queryset.
    def get_webinars_by_profileId_or_ids(self, request: Request):
        # if profile is provided.
        profileId = request.query_params.get('profile_id')

        qs: QuerySet
        if profileId:
            if request.user.is_anonymous:
                raise NotAuthenticated(detail=None, code=None)
            # check if the requested profile id matched the auth user
            profile = get_profile_by_user(request.user)
            # if profile matched, filter the webinars saved by the user
            print(profile.id.__str__() == profileId)
            if profile.id.__str__() == profileId:
                qs = self.queryset.filter(savedBy=profile)
            else:
                qs = self.get_queryset()

        else:
            # when profileId (for logged in users) is not provided, check if ids is provided in the get request json body: for unloggedin users to get saved webinars.
            # eg. { "ids": [ "uuid1", "uuid2" ] }
            if 'ids' in request.data:
                ids = request.data['ids']
                print(ids)
                qs = self.queryset.filter(id__in=ids)
            # when neither profile id nor json ids array are provided
            else:
                qs = self.get_queryset()
        return qs

    # filter webianrs by week
    def get_month_webinars(self, request: Request) -> QuerySet:
        now = datetime.datetime.now()
        last_2h = now - datetime.timedelta(hours=2)
        next_31d = now + datetime.timedelta(days=31)
        return self.get_webinars_by_range(request, last_2h, next_31d)

    # filter webianrs by week
    def get_week_webinars(self, request: Request) -> QuerySet:
        now = datetime.datetime.now()
        last_2h = now - datetime.timedelta(hours=2)
        next_7d = now + datetime.timedelta(days=7)
        return self.get_webinars_by_range(request, last_2h, next_7d)

    # filter webinars by tomorrow
    def get_day_recommend_webinars(self, request: Request, day_start, day_end) -> QuerySet:

        # tz_today: datetime.datetime = datetime.datetime.now(pytz.timezone(timezone)).today()
        # tz_tomorrow = (tz_today.astimezone(pytz.timezone(timezone)) + datetime.timedelta(days=1))
        # tomorrow_start = datetime.datetime.combine(tz_tomorrow, datetime.time.min)
        # tomorrow_end = datetime.datetime.combine(tz_tomorrow, datetime.time.max)
        # print(tomorrow_start.astimezone(pytz.utc).__str__())
        # print(tomorrow_end.astimezone(pytz.utc).__str__())
        return self.get_webinars_by_range(request, day_start.__str__(), day_end.__str__())

    # filter webinars by today
    def get_today_webinars(self, request: Request) -> QuerySet:
        now = datetime.datetime.now()
        last_2h = now - datetime.timedelta(hours=2)
        next_24h = now + datetime.timedelta(hours=24)
        return self.get_webinars_by_range(request, last_2h, next_24h)



    # def filter_webinars_by_tags(self, queryset: QuerySet, request: Request) -> QuerySet:
    #     """
    #     generate filter for webinars by tags.
    #     :param queryset:
    #     :param request:
    #     :return: Queryset
    #     """
    #     # logger.error(request.data)
    #     # if the post request provides tag ids
    #     try:
    #         # parse request json body
    #         body_unicode = request.body.decode('utf-8')
    #         body_data = json.loads(body_unicode)
    #         # extract array of tag uuid strings.
    #         tag_ids: [str] = body_data['tagIds']
    #         # filter
    #         result: QuerySet = queryset.filter(tags__in=tag_ids)
    #         return result
    #     # if any error occurs, raise the exception and let the handlers return corresponding errors
    #     except:
    #         raise

    def return_filtered_and_paginated_qs(self, qs: QuerySet) -> Response:
        # then use default filterSet to handle other filters like tags, startdatetime or organizers
        qs = self.filter_queryset(qs)
        # paginate
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        # if no pagination (which is currently applied globally), return all retulst
        webinars_str = self.get_serializer(qs, many=True).data
        return Response(webinars_str)

    # def get_some_webinar_by_tags(self, webinars: QuerySet, request: Request) -> Response:
    #     """
    #     generate help request handler for webinar-tag filter requests
    #     :param webinars: super queryset from which to filter by tags
    #     :param request: must has "tagIds" property in the json payload
    #     :return: http response with data or error
    #     """
    #     try:
    #         webinars: QuerySet = self.filter_webinars_by_tags(webinars, request)
    #         serializer = self.get_serializer(webinars, many=True)
    #         return Response(serializer.data)
    #     except JSONDecodeError:
    #         return Response("bad json request", status=status.HTTP_400_BAD_REQUEST)
    #     except KeyError:
    #         return Response("no tagids found in the payload", status=status.HTTP_400_BAD_REQUEST)
    #     # notice the validation error is defined in Django core exceptions, not in DRF.
    #     except ValidationError:
    #         return Response("provided tag ids are incorrect", status=status.HTTP_400_BAD_REQUEST)
