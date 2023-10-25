"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from dj_rest_auth.registration.views import VerifyEmailView
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from djangoProject.lead.views import LeadPostView
from djangoProject.report.views import ReportViewSet
from djangoProject.sources.views import SourcePostView
from djangoProject.tag.views import TagListView
from djangoProject.userprofile.views import UserProfileViewSet
from djangoProject.webinar.views import WebinarViewSet

router = routers.DefaultRouter()

router.register(r'webinars', WebinarViewSet)
router.register(r'leads', LeadPostView)
router.register(r'userprofiles', UserProfileViewSet)
router.register(r'report', ReportViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    ##


    # generic api views
    path('tags/', TagListView.as_view(), name='tags'),
    path('sources/', SourcePostView.as_view(), name='sources'),


    path('password-reset/confirm/<uidb64>/<token>/', TemplateView.as_view(), name='password_reset_confirm'),
    # for account-confirm-email.
    path('auth/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('auth/', include('dj_rest_auth.urls')),
    path('register/', include('dj_rest_auth.registration.urls')),
    url(r'^admin/clearcache/', include('clearcache.urls')),
    url(r'^accounts/', include('allauth.urls')),


    path('__debug__/', include(debug_toolbar.urls)),
]
