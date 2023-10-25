from django_filters import rest_framework as filters, DateTimeFromToRangeFilter

from djangoProject.webinar.models import Webinar


# class WebinarTodayFilter(filters.FilterSet):
#     startDateTime = DateTimeFromToRangeFilter()
#
#     class Meta:
#         model = Webinar
#         fields = ['tags', 'startDateTime', 'organizers']
#
#     # request based query
#     @property
#     def qs(self):
#         parent = super().qs
#         user = getattr(self.request, 'user', None)
#         profile = get_profile_by_user(user)
#         # author = getattr(self.request, 'user', None)
#
#         return parent.filter(savedBy=profile)

class WebinarFilter(filters.FilterSet):
    startDateTimeUTC = DateTimeFromToRangeFilter()

    class Meta:
        model = Webinar
        fields = [
            'tags',
            'startDateTimeUTC',
            'organizers',
            'tagCount',
            'participants',
            'talks__speakers__person',
            'hasRecordingOrTranscript',
            'recommend',
            'recommended',
            'hosts',
            'hosts__organizations',
            'hostOrganizations'
        ]


    # request based query
    # @property
    # def qs(self):
    #     parent = super().qs
    #     # if self.request is not None:
    #     #     tags = getattr(self.request, 'tag', None)
    #     #     return parent.filter(tags=tags)
    #     return parent