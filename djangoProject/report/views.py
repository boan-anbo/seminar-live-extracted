# Create your views here.
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from djangoProject.report.filters import ReportFilter
from djangoProject.report.models import Report
from djangoProject.report.serializers import ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class=ReportFilter

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        # only allow user to create. restrict other methods to the admin.
        if self.action == 'create':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
