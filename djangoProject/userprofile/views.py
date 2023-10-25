# Create your views here.
from typing import cast

from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django_filters import rest_framework as filters
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.request import Request
from rest_framework.response import Response

from djangoProject.userprofile.actions import get_profile_by_user
from djangoProject.userprofile.filters import UserProfileFilter
from djangoProject.userprofile.models import UserProfile
from djangoProject.userprofile.serializers import UserProfileSerializer
from djangoProject.webinar.models import Webinar


@receiver(post_save, sender=User)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        UserProfile.objects.get_or_create(user=kwargs.get('instance'))
        print("created profile for the user")


class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj.owner == request.user
        else:
            return False

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by('id')
    serializer_class = UserProfileSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class=UserProfileFilter
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsSuperUser, ]
        elif self.action == 'retrieve':
            self.permission_classes = [IsOwner]
        return super(self.__class__, self).get_permissions()

    @action(detail=False, methods=['get'], permission_classes = [])
    def send_email(self, request: Request):
        send_mail(
            'Subject here',
            'Here is the message.',
            'no-reply@seminar-live.com',
            ['test@seminar-live.com', 'gazagoal@gmail.com'],
            fail_silently=False,
        )
        return Response("DONE")

    @action(detail=False, methods=['post'])
    def update_settings(self, request: Request):
        update_profile = cast(UserProfile, request.data)

        try:
            profile = get_profile_by_user(request.user)
            print(profile.id)
            update_language = update_profile['language']
            update_timezone = update_profile['timezone']
            if update_language:
                profile.language = update_language
            if update_timezone:
                profile.timezone = update_timezone
            profile.save()
            print(profile.language)
            # profile_str = UserProfileSerializer(profile, many=False).data
            return Response(    status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    # show user profile
    @action(detail=False, methods=['get'])
    def mine(self, request: Request):
        profile_str = self.get_serializer(UserProfile.objects.get(user=request.user)).data
        return Response(profile_str)


    @action(detail=False, methods=['get'],
            url_path='save/(?P<webinarId>[^/.]+)'
            )
    def save(self, request: Request, webinarId):

        try:
            profile: UserProfile = UserProfile.objects.get(user=request.user)
            self.add_one_webinar_to_profile(profile, webinarId)
            return Response("added successful", status=status.HTTP_200_OK)
        except:
            return HttpResponse("error saving webinar", status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'] ,
             url_path='push')
    def push(self, request: Request):
        # jsonObject = json.load(request.data)
        try:
            ids = request.data['ids']
            profile: UserProfile = UserProfile.objects.get(user=request.user)
            for id in ids:
                try:
                    self.add_one_webinar_to_profile(profile, id)
                except:
                    pass
        except KeyError:
            return HttpResponse("", status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return HttpResponse("Wrong webinar ids", status=status.HTTP_400_BAD_REQUEST)
        responseProfile = get_profile_by_user(request.user)
        responseProfile_str = self.get_serializer(responseProfile, many=False).data
        return Response(responseProfile_str, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'],
            url_path='unsave/(?P<webinarId>[^/.]+)'
            )
    def unsave(self, request: Request, webinarId):
        try:
            profile: UserProfile = UserProfile.objects.get(user=request.user)
            webinar = Webinar.objects.get(id=webinarId)
            if not profile.savedWebinars.filter(id=webinar.id).exists():
                return Response("webinar is not saved before", status=status.HTTP_208_ALREADY_REPORTED)
            profile.savedWebinars.remove(webinar)
            profile.save()
            return Response("unsaved successful", status=status.HTTP_200_OK)
        except:
            return Response("error unsaving webinar", status=status.HTTP_400_BAD_REQUEST)

    def add_one_webinar_to_profile(self, profile: UserProfile, webinarId):
        webinar = Webinar.objects.get(id=webinarId)
        if profile.savedWebinars.filter(id=webinar.id).exists():
            return HttpResponse("already added", status=status.HTTP_208_ALREADY_REPORTED)
        profile.savedWebinars.add(webinar)
        profile.save()


    @action(detail=False, methods=['post'], permission_classes=[])
    def reset_password(self, request: Request):
        try:
            email = request.data['email']

            print(email)
        # profile_str = self.get_serializer(UserProfile.objects.get(user=request.user)).data
            return Response('')
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'], permission_classes = [])
    def resent_verification_email(self, request: Request):
        user = get_object_or_404(User, email=request.data['email'])
        emailAddress = EmailAddress.objects.filter(user=user, verified=True).exists()

        if emailAddress:
            # I'm leaving response message for "account already verified" empty to prevent probing
            return Response('', status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                send_email_confirmation(request, user=user)
                # {'message': 'Email confirmation sent'}
                return Response('', status=status.HTTP_201_CREATED)
            except APIException:
                # {'message': 'This email does not exist, please create a new account'}
                return Response('',
                                status=status.HTTP_403_FORBIDDEN)