# Create your views here.

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from djangoProject.lead.actions import get_data_from_zoom, get_data_from_eventbrite, get_data_from_hnet
from djangoProject.lead.filters import LeadFilter
from djangoProject.lead.models import Lead
from djangoProject.lead.permissions import IsLeadCollector, LeadPermission
from djangoProject.lead.serializers import LeadSerializer
from djangoProject.webinar.persmission_custom import IsDirectPoster


@receiver(post_save, sender=Lead)
def default_lead_status_to_inactive(sender, instance, **kwargs):
    if kwargs.get('created', False):
        instance.status = False
        instance.save()




class LeadPostView(viewsets.ModelViewSet):
    # this empty the project setting for authentications in order to easy the CSRF token authentication for Post, i.e. when you try to post leads.
    # authentication_classes = []

    queryset = Lead.objects.all().order_by('created')
    serializer_class = LeadSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = LeadFilter
    permission_classes = [LeadPermission]


    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated, IsLeadCollector]
    )
    def get_leads(self, request):
        leads = Lead.objects.filter(status=False).order_by('-created')

        leads_payload = LeadSerializer(leads, many=True).data

        return Response(leads_payload, status=status.HTTP_200_OK)


    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsLeadCollector]
    )
    def parse_zoom(self, request):
        url = request.data.get('url')
        if url:
            response = get_data_from_zoom(url)
            return Response(response, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsLeadCollector]
    )
    def parse_hnet(self, request):
        url = request.data.get('url')
        if url:
            response = get_data_from_hnet(url)
            return Response(response, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsLeadCollector]
    )
    def parse_eventbrite(self, request):
        url = request.data.get('url')
        if url:
            response = get_data_from_eventbrite(url)
            return Response(response, status=status.HTTP_200_OK)


# renderer_classes = [TemplateHTMLRenderer]

# @action(detail=True)
# def preview(self, request, pk):
#     jsonStr = self.get_object().json
#     json_data = json.loads(jsonStr)
#     json_pretty = json.dumps(json_data, sort_keys=True, indent=4)
#     return HttpResponse(json_pretty, content_type='application/json')
